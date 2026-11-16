#!/usr/bin/env bash
# this_file: build.sh
#
# Build opentype-feature-freezer sdist + wheel into dist/. The version comes from git tags
# via hatch-vcs, so an untagged or dirty tree builds a .devN version.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

rm -rf dist
uv build
ls -l dist
