import logging
import os
from types import SimpleNamespace
from typing import List, Mapping, MutableMapping, Optional, Set

import fontTools.ttLib as ttLib

__version__ = "1.32.2"


logger = logging.getLogger(__name__)


class RemapByOTL:
    def __init__(self, options: SimpleNamespace):
        self.inpath: os.PathLike = options.inpath
        self.outpath: os.PathLike = options.outpath
        if not self.outpath:
            self.outpath = os.fspath(self.inpath) + ".featfreeze.otf"
        self.FeatureIndex = None
        self.filterByFeatures = None
        self.filterByLangSys = None
        self.filterByScript = None
        self.LookupList = None
        self.names: List[str] = []
        self.options: SimpleNamespace = options
        self.reportFeature: List[str] = []
        self.reportLangSys: List[str] = []
        self.subs0: List[str] = []
        self.subs1: List[str] = []
        self.substitution_mapping: MutableMapping[str, str] = {}
        self.success: bool = True
        self.ttx: Optional[ttLib.TTFont] = None
        logger.info("[RemapByOTL] Running with options: %s", self.options)

    def openFont(self):
        self.success = True
        self._openFontTTX()
        if not self.ttx:
            self.success = False
        if self.success:
            logger.info("[openFont] Opened font: %s", self.inpath)

    def _openFontTTX(self):
        self.success = True
        if self.inpath:
            try:
                self.ttx = ttLib.TTFont(self.inpath, 0, recalcBBoxes=False)
            except Exception as e:
                logger.warning(
                    "[_openFontTTX] TTX cannot open %s: %s", self.inpath, e)
                self.success = False
                self.ttx = None

    def saveFont(self):
        if self.options.report:
            self._reportFont()
        else:
            if self.options.zapnames:
                self.ttx["post"].formatType = 3.0
            self._saveFontTTX()
            if self.success:
                logger.info("[saveFont] Saved font: %s", self.outpath)

    def _reportFont(self):
        self.success = True
        print(
            "# Scripts and languages:\n%s"
            % ("\n".join(sorted(list(set(self.reportLangSys)))))
        )
        print("# Features:\n-f %s" %
              (",".join(sorted(list(set(self.reportFeature))))))

    def _saveFontTTX(self):
        self.success = True
        outpath = self.outpath
        try:
            self.ttx.save(outpath)
        except Exception as e:
            logger.warning("[_saveFontTTX] TTX cannot save %s: %s", outpath, e)
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
        self.filterByScript = self.options.script
        self.filterByLangSys = self.options.lang
        if "GSUB" not in self.ttx:
            logger.warning(
                "No 'GSUB' table found in %s, nothing to do!", self.inpath)
            self.success = True
            return

        gsub = self.ttx["GSUB"].table
        self.FeatureIndex = []
        for ScriptRecord in gsub.ScriptList.ScriptRecord:
            if self.options.report:
                self.reportLangSys.append("-s '%s'" % (ScriptRecord.ScriptTag))
                for LangSysRecord in ScriptRecord.Script.LangSysRecord:
                    self.reportLangSys.append(
                        "-s '%s' -l '%s'"
                        % (ScriptRecord.ScriptTag, LangSysRecord.LangSysTag)
                    )
            if (ScriptRecord.ScriptTag == self.filterByScript) or not self.filterByScript:
                if self.filterByLangSys:
                    for LangSysRecord in ScriptRecord.Script.LangSysRecord:
                        if LangSysRecord.LangSysTag == self.filterByLangSys:
                            self.FeatureIndex += LangSysRecord.LangSys.FeatureIndex
                else:
                    self.FeatureIndex += ScriptRecord.Script.DefaultLangSys.FeatureIndex
        self.FeatureIndex = sorted(list(set(self.FeatureIndex)))
        logger.info("[filterFeatureIndex] FeatureIndex: %s", self.FeatureIndex)

    def filterLookupList(self):
        self.success = True
        self.filterByFeatures = self.options.features.split(",")
        logger.info("[filterLookupList] Features to apply: %s",
                    self.filterByFeatures)
        if "GSUB" not in self.ttx:
            self.success = True
            return

        gsub = self.ttx["GSUB"].table
        self.LookupList = []
        if self.options.report:
            for FeatureRecord in gsub.FeatureList.FeatureRecord:
                self.reportFeature.append(FeatureRecord.FeatureTag)
        for fi in self.FeatureIndex:
            if gsub.FeatureList.FeatureRecord[fi].FeatureTag in self.filterByFeatures:
                self.LookupList += gsub.FeatureList.FeatureRecord[
                    fi
                ].Feature.LookupListIndex
        self.LookupList = sorted(list(set(self.LookupList)))
        logger.info("[filterLookupList] Lookups: %s", self.LookupList)

    def applySubstitutions(self):
        self.success = True
        if "GSUB" not in self.ttx:
            self.success = True
            return

        # Determine which glyphs have any Unicode value attached at all, to warn the
        # user when trying to freeze glyph substitutions where neither has a Unicode
        # value and therefore nothing will happen.
        glyphs_with_unicode_value: Set[str] = {
            glyph_name
            for cmap_table in self.ttx["cmap"].tables
            for glyph_name in cmap_table.cmap.values()
        }

        # Work out the substitutions.
        gsub = self.ttx["GSUB"].table
        for LookupID in self.LookupList:
            Lookup = gsub.LookupList.Lookup[LookupID]
            for Subtable in Lookup.SubTable:
                if Subtable.LookupType not in {1, 3, 7}:
                    continue  # Can't handle anything else.

                mapping: Mapping[str, str]
                alternates: Mapping[str, str]
                mapping = alternates = {}
                if Subtable.LookupType == 1:
                    mapping = Subtable.mapping
                elif Subtable.LookupType == 3:
                    alternates = Subtable.alternates
                elif Subtable.LookupType == 7:
                    ExtSubTable = Subtable.ExtSubTable
                    if ExtSubTable.LookupType == 1:
                        mapping = ExtSubTable.mapping
                    elif ExtSubTable.LookupType == 3:
                        alternates = ExtSubTable.alternates

                for sub_in, sub_out in mapping.items():
                    for i in range(len(self.subs1)):
                        if self.subs1[i] == sub_in:
                            self.subs1[i] = sub_out

                # Always take the first alternate.
                for sub_in, sub_out_class in alternates.items():
                    sub_out_first = sub_out_class[0]
                    for i in range(len(self.subs1)):
                        if self.subs1[i] == sub_in:
                            self.subs1[i] = sub_out_first

        if len(self.subs0) != len(self.subs1):
            raise RuntimeError(
                "Internal error: Substitution mapping out of sync.")

        # Zip the above mappings together.
        for sub_in, sub_out in zip(self.subs0, self.subs1):
            self.substitution_mapping[sub_in] = sub_out
            if sub_in != sub_out:
                if (
                    sub_in not in glyphs_with_unicode_value
                    and sub_out not in glyphs_with_unicode_value
                ):
                    logger.warning(
                        "[applySubstitutions] Cannot remap '%s' -> '%s' because "
                        "neither has a Unicode value assigned in any of the "
                        "cmap tables.",
                        sub_in,
                        sub_out,
                    )
                    continue

                if self.options.names:
                    self.names.append(sub_out)

                logger.info(
                    "[applySubstitutions] Remap: '%s' -> '%s'", sub_in, sub_out)

    def remapCmaps(self):
        self.success = True
        cmap = self.ttx["cmap"]
        for cmaptable in cmap.tables:
            for u in cmaptable.cmap:
                cmaptable.cmap[u] = self.substitution_mapping[cmaptable.cmap[u]]

    def renameFont(self):
        self.success = True
        if not self.options.suffix and not self.options.replacenames:
            return self.success

        name: ttLib.tables._n_a_m_e.table__n_a_m_e = self.ttx["name"]

        # First, determine the canonical family name. Assume that the font is storing
        # its primary name records for the Windows platform with the Unicode BMP
        # encoding. Take it from the first language we find. Disregard the WWS Family
        # Name, as it is little used. Assume that the family name is the same for all
        # languages.
        family_name: str = (name.getName(16, 3, 1) or name.getName(1, 3, 1)).toStr()
        family_name_old = family_name
        family_name_no_space = family_name.replace(" ", "")
        family_name_no_space_old = family_name_no_space

        # Mutate the family name, e.g. for fulfilling the OFL Reserved Font
        # Name(s) clause.
        if self.options.replacenames:
            for search, replace in [
                s.split("/") for s in self.options.replacenames.split(",")
            ]:
                family_name = family_name.replace(search, replace)

        # A suffix to appended to a family name. Use the provided one, otherwise
        # generate it from the selected features.
        if self.options.usesuffix:
            suffix = f" {self.options.usesuffix}"
        elif self.options.suffix:
            suffix = " ".join(sorted(self.filterByFeatures))
            if suffix:  # Add padding space if we actually have a suffix.
                suffix = f" {suffix}"
        else:
            suffix = ""

        family_name_new = f"{family_name}{suffix}"
        family_name_new_no_space = family_name_new.replace(" ", "")

        for record in name.names:
            if record.nameID in {1, 4, 16, 18, 21}:
                record.string = record.toStr().replace(family_name_old, family_name_new)
            elif record.nameID == 3:
                # Unique ID. Do not search and replace strings here because a unique ID
                # is essentially an arbitrary string.
                record.string = f"{record.toStr()};featfreeze:{self.options.features}"
            elif record.nameID == 5 and self.options.info:
                # Version string. Do not search and replace strings here because the
                # field is a semi-arbitrary string.
                record.string = f"{record.toStr()}; featfreeze: {self.options.features}"
            elif record.nameID in (6, 20):
                # PostScript name: no spaces.
                record.string = record.toStr().replace(
                    family_name_no_space_old, family_name_new_no_space
                )

        full_name_new = name.getName(4, 3, 1).toStr()
        postscript_name_new = name.getName(6, 3, 1).toStr()

        if "CFF " in self.ttx:
            cff = self.ttx["CFF "].cff
            if len(cff.fontNames) > 1:
                raise RuntimeError(
                    "Cannot properly rename font with multiple CFF font entries"
                )

            top_dict = cff[0].rawDict
            top_dict["FamilyName"] = family_name_new.encode("utf-8")
            top_dict["FullName"] = full_name_new.encode("utf-8")
            cff.fontNames[0] = postscript_name_new.encode("utf-8")

        logger.info("[renameFont] New family name: '%s'", family_name_new)
        logger.info("[renameFont] New full name: '%s'", full_name_new)
        logger.info("[renameFont] New PostScript name: '%s'",
                    postscript_name_new)

        return self.success

    def remapByOTL(self):
        self.success = True
        self.initSubs()
        if self.success:
            self.filterFeatureIndex()
        if self.success:
            self.filterLookupList()
        if self.success:
            self.applySubstitutions()
        if self.success:
            self.remapCmaps()
        if self.success:
            if self.options.names:
                print(" ".join(self.names))

    def run(self):
        self.openFont()
        if not self.success:
            return

        self.remapByOTL()
        if self.success:
            self.renameFont()
        if self.success:
            self.saveFont()
        self.closeFont()
