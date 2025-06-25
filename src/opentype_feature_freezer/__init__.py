import logging
import os
from collections.abc import Mapping, MutableMapping
from types import SimpleNamespace
from typing import List, Optional, Set

import fontTools.ttLib as ttLib

__version__ = "1.32.2"


logger = logging.getLogger(__name__)


class RemapByOTL:
    def __init__(self, options: Namespace):  # Changed SimpleNamespace to Namespace
        self.inpath: os.PathLike = options.inpath
        self.outpath: os.PathLike = options.outpath
        if not self.outpath:
            self.outpath = os.fspath(self.inpath) + ".featfreeze.otf"
        self.FeatureIndex = None
        self.filterByFeatures = None
        self.filterByLangSys = None
        self.filterByScript = None
        self.LookupList = None
        self.names: list[str] = []
        self.options: SimpleNamespace = options
        self.reportFeature: list[str] = []
        self.reportLangSys: list[str] = []
        self.subs0: list[str] = []
        self.subs1: list[str] = []
        self.substitution_mapping: MutableMapping[str, str] = {}
        self.success: bool = True
        self.ttx: ttLib.TTFont | None = None
        logger.info("[RemapByOTL] Running with options: %s", self.options)

    def openFont(self):
        self.success = True
        self._openFontTTX()
        if not self.ttx:
            self.success = False
        if self.success:
            logger.info(f"[openFont] Opened font: {self.inpath}")

    def _openFontTTX(self):
        self.success = True
        if self.inpath:
            try:
                self.ttx = ttLib.TTFont(self.inpath, 0, recalcBBoxes=False)
            except Exception as e:
                logger.warning("[_openFontTTX] TTX cannot open %s: %s", self.inpath, e)
                self.success = False
                self.ttx = None

    def saveFont(self):
        if self.options.report:
            self._reportFont()
        else:
            if self.options.zapnames:
                assert self.ttx is not None  # Ensured by successful openFont
                self.ttx["post"].formatType = 3.0
            self._saveFontTTX()
            if self.success:
                logger.info(f"[saveFont] Saved font: {self.outpath}")

    def _reportFont(self):
        self.success = True
        print(
            "# Scripts and languages:\n%s"
            % ("\n".join(sorted(list(set(self.reportLangSys)))))
        )
        print("# Features:\n-f %s" % (",".join(sorted(list(set(self.reportFeature))))))

    def _saveFontTTX(self):
        self.success = True
        outpath = self.outpath
        try:
            assert self.ttx is not None  # Ensured by successful openFont
            self.ttx.save(outpath)
        except Exception as e:
            logger.warning(f"[_saveFontTTX] TTX cannot save {outpath}: {e}")
            self.success = False

    def closeFont(self):
        self.success = True
        self._closeFontTTX()

    def _closeFontTTX(self):
        self.success = True
        if self.ttx:
            self.ttx.close()

    def initSubs(self):
        self.success = True
        self.subs0 = list(self.ttx.getGlyphOrder())
        self.subs1 = list(self.ttx.getGlyphOrder())

    def filterFeatureIndex(self):
        self.success = True
        assert self.ttx is not None  # Ensured by successful openFont
        self.filterByScript = self.options.script
        self.filterByLangSys = self.options.lang
        if "GSUB" not in self.ttx:
            logger.warning("No 'GSUB' table found in %s, nothing to do!", self.inpath)
            self.success = True
            return

        gsub = self.ttx["GSUB"].table
        feature_index_set: Set[int] = set()  # More precise type
        for ScriptRecord in gsub.ScriptList.ScriptRecord:
            if self.options.report:
                self.reportLangSys.append(f"-s '{ScriptRecord.ScriptTag}'")
                for LangSysRecord in ScriptRecord.Script.LangSysRecord:
                    self.reportLangSys.append(
                        f"-s '{ScriptRecord.ScriptTag}' -l '{LangSysRecord.LangSysTag}'"
                    )
            if (
                ScriptRecord.ScriptTag == self.filterByScript
            ) or not self.filterByScript:
                if self.filterByLangSys:
                    for LangSysRecord in ScriptRecord.Script.LangSysRecord:
                        if LangSysRecord.LangSysTag == self.filterByLangSys:
                            feature_index_set.update(LangSysRecord.LangSys.FeatureIndex)
                else:
                    feature_index_set.update(
                        ScriptRecord.Script.DefaultLangSys.FeatureIndex
                    )
            self.FeatureIndex: List[int] = sorted(
                feature_index_set
            )  # Keep as List[int]
        logger.info(f"[filterFeatureIndex] FeatureIndex: {self.FeatureIndex}")

    def filterLookupList(self):
        self.success = True
        assert self.ttx is not None  # Ensured by successful openFont
        self.filterByFeatures = self.options.features.split(",")
        logger.info("[filterLookupList] Features to apply: %s", self.filterByFeatures)
        if "GSUB" not in self.ttx:
            self.success = True
            return

        gsub = self.ttx["GSUB"].table
        lookup_list_set: Set[int] = set()  # More precise type
        if self.options.report:
            for FeatureRecord in gsub.FeatureList.FeatureRecord:
                self.reportFeature.append(FeatureRecord.FeatureTag)

        assert (
            self.FeatureIndex is not None
        )  # Should be populated by filterFeatureIndex
        for fi in self.FeatureIndex:
            if gsub.FeatureList.FeatureRecord[fi].FeatureTag in self.filterByFeatures:
                lookup_list_set.update(
                    gsub.FeatureList.FeatureRecord[fi].Feature.LookupListIndex
                )
        self.LookupList: List[int] = sorted(lookup_list_set)  # Keep as List[int]
        logger.info(f"[filterLookupList] Lookups: {self.LookupList}")

    def applySubstitutions(self):
        self.success = True
        assert self.ttx is not None  # Ensured by successful openFont
        if "GSUB" not in self.ttx:
            self.success = True
            return

        # Determine which glyphs have any Unicode value attached at all, to warn the
        # user when trying to freeze glyph substitutions where neither has a Unicode
        # value and therefore nothing will happen.
        glyphs_with_unicode_value: set[str] = {
            glyph_name
            for cmap_table in self.ttx["cmap"].tables
            for glyph_name in cmap_table.cmap.values()
        }

        # Work out the substitutions.
        gsub = self.ttx["GSUB"].table
        assert self.LookupList is not None  # Should be populated by filterLookupList
        for LookupID in self.LookupList:
            Lookup = gsub.LookupList.Lookup[LookupID]
            for Subtable in Lookup.SubTable:
                if Subtable.LookupType not in {1, 3, 7}:
                    continue  # Can't handle anything else.

                mapping: Mapping[str, str] = {}
                alternates: Mapping[str, List[str]] = {}  # Type for alternates

                if Subtable.LookupType == 1:
                    mapping = Subtable.mapping
                elif Subtable.LookupType == 3:
                    alternates = Subtable.alternates
                elif Subtable.LookupType == 7:  # Extension lookup
                    ExtSubTable = Subtable.ExtSubTable
                    if ExtSubTable.LookupType == 1:
                        mapping = ExtSubTable.mapping
                    elif ExtSubTable.LookupType == 3:
                        alternates = ExtSubTable.alternates

                for sub_in, sub_out in mapping.items():
                    for i, current_glyph in enumerate(self.subs1):
                        if current_glyph == sub_in:
                            self.subs1[i] = sub_out

                # Always take the first alternate.
                for sub_in, sub_out_glyph_list in alternates.items():
                    if sub_out_glyph_list:  # Ensure there is at least one alternate
                        sub_out_first = sub_out_glyph_list[0]
                        for i, current_glyph in enumerate(self.subs1):
                            if current_glyph == sub_in:
                                self.subs1[i] = sub_out_first

        if len(self.subs0) != len(self.subs1):
            raise RuntimeError("Internal error: Substitution mapping out of sync.")

        # Zip the above mappings together.
        for sub_in, sub_out in zip(self.subs0, self.subs1):
            self.substitution_mapping[sub_in] = sub_out
            if sub_in != sub_out:
                if (
                    sub_in not in glyphs_with_unicode_value
                    and sub_out not in glyphs_with_unicode_value
                ):
                    logger.warning(
                        f"[applySubstitutions] Cannot remap '{sub_in}' -> '{sub_out}' "
                        "because neither has a Unicode value assigned in any of the "
                        "cmap tables."
                    )
                    continue

                if self.options.names:
                    self.names.append(sub_out)

                logger.info("[applySubstitutions] Remap: '%s' -> '%s'", sub_in, sub_out)

    def remapCmaps(self):
        self.success = True
        assert self.ttx is not None  # Ensured by successful openFont
        cmap = self.ttx["cmap"]
        for cmaptable in cmap.tables:
            # Mypy needs help understanding cmaptable.cmap is a MutableMapping[int, str]
            current_cmap: MutableMapping[int, str] = cmaptable.cmap
            for u_code, glyph_name in list(
                current_cmap.items()
            ):  # Iterate over a copy for modification
                current_cmap[u_code] = self.substitution_mapping.get(
                    glyph_name, glyph_name
                )

    def renameFont(self):
        self.success = True
        assert self.ttx is not None  # Ensured by successful openFont
        if not self.options.suffix and not self.options.replacenames:
            return self.success  # Return True explicitly

        name_table: ttLib.tables._n_a_m_e.table__n_a_m_e = self.ttx["name"]

        # First, determine the canonical family name. Assume that the font is storing
        # its primary name records for the Windows platform with the Unicode BMP
        # encoding. Take it from the first language we find. Disregard the WWS Family
        # Name, as it is little used. Assume that the family name is the same for all
        # languages.
        name_record_16 = name_table.getName(16, 3, 1)
        name_record_1 = name_table.getName(1, 3, 1)
        primary_name_record = name_record_16 if name_record_16 else name_record_1

        if not primary_name_record:
            # Fallback or error if no primary name record is found
            logger.error("Could not determine primary family name from name table.")
            # Attempt to use the first available family name or a default
            family_name = "UnknownFamily"
            for record in name_table.names:
                if record.nameID == 1:  # NameID 1: Family Name
                    family_name = record.toStr()
                    break
        else:
            family_name = primary_name_record.toStr()

        family_name_old = family_name
        family_name_no_space = family_name.replace(" ", "")
        family_name_no_space_old = family_name_no_space

        # Mutate the family name, e.g. for fulfilling the OFL Reserved Font
        # Name(s) clause.
        if self.options.replacenames:
            # Ensure replacenames is a string before splitting
            replace_items_str = self.options.replacenames or ""
            for item in replace_items_str.split(","):
                if not item:
                    continue
                parts = item.split("/", 1)  # Ensure splitting only once
                if len(parts) == 2:
                    search, replace = parts
                    family_name = family_name.replace(search, replace)
                else:
                    logger.warning(
                        f"Invalid format in replacenames: '{item}'. "
                        "Expected 'search/replace'."
                    )

        # A suffix to appended to a family name. Use the provided one, otherwise
        # generate it from the selected features.
        suffix_str = ""
        if self.options.usesuffix:
            suffix_str = f" {self.options.usesuffix}"
        elif self.options.suffix:
            # filterByFeatures should be List[str] as per earlier logic,
            # ensure it's not None
            features_for_suffix = self.filterByFeatures or []
            if features_for_suffix:
                # Sort features for consistent suffix generation
                suffix_str = " " + " ".join(sorted(features_for_suffix)) # Added space

        family_name_new = f"{family_name}{suffix_str}"
        family_name_new_no_space = family_name_new.replace(" ", "")

        for record in name_table.names:
            record_str = record.toStr()  # Cache to avoid multiple calls
            if record.nameID in {
                1,
                4,
                16,
                18,
                21,
            }:  # Family, Full, WWS Family, WWS Subfamily, Light Background Palette
                record.string = record_str.replace(family_name_old, family_name_new)
            elif record.nameID == 3:  # Unique ID
                record.string = f"{record_str};featfreeze:{self.options.features}"
            elif record.nameID == 5 and self.options.info:  # Version string
                record.string = f"{record_str}; featfreeze: {self.options.features}"
            elif record.nameID in {
                6,
                20,
            }:  # PostScript name, PostScript CID findfont name
                record.string = record_str.replace(
                    family_name_no_space_old, family_name_new_no_space
                )

        # Re-fetch potentially changed names for CFF table
        full_name_new_obj = name_table.getName(4, 3, 1)
        postscript_name_new_obj = name_table.getName(6, 3, 1)

        full_name_new = (
            full_name_new_obj.toStr() if full_name_new_obj else family_name_new
        )
        postscript_name_new = (
            postscript_name_new_obj.toStr()
            if postscript_name_new_obj
            else family_name_new_no_space
        )

        if "CFF " in self.ttx:
            cff_table = self.ttx["CFF "].cff  # Corrected to cff_table
            if len(cff_table.fontNames) > 1:
                logger.warning(
                    "Font has multiple CFF font entries. Renaming only the first one."
                )

            top_dict = cff[0].rawDict
            top_dict["FamilyName"] = family_name_new.encode("utf-8")
            top_dict["FullName"] = full_name_new.encode("utf-8")
            cff.fontNames[0] = postscript_name_new.encode("utf-8")

        logger.info("[renameFont] New family name: '%s'", family_name_new)
        logger.info("[renameFont] New full name: '%s'", full_name_new)
        logger.info("[renameFont] New PostScript name: '%s'", postscript_name_new)

        return self.success

    def remapByOTL(self):
        # No specific changes needed here, logic is sequential calls.
        # self.success is checked by each called method.
        self.success = True  # Start with success
        self.initSubs()
        if not self.success:
            return

        self.filterFeatureIndex()
        if not self.success:
            return

        self.filterLookupList()
        if not self.success:
            return

        self.applySubstitutions()
        if not self.success:
            return

        self.remapCmaps()
        if not self.success:
            return

        if self.options.names:  # This check can remain as is
            # Ensure self.names is not None if used, though it's initialized as []
            print(" ".join(self.names or []))

    def run(self):
        # Logic is sequential, driven by self.success flag.
        # This structure is clear and fine.
        self.openFont()
        if not self.success:
            logger.error("Failed to open font. Aborting.")
            return

        self.remapByOTL()
        if not self.success:
            logger.error("Failed during OpenType Layout remapping. Aborting.")
            return

        self.renameFont()
        if not self.success:
            logger.error("Failed during font renaming. Aborting.")
            return

        self.saveFont()
        if not self.success:
            logger.error("Failed to save font.")
            # self.closeFont() will still be called after this block

        self.closeFont()  # Ideally in a finally block
