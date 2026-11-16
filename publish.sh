#!/usr/bin/env bash
# this_file: publish.sh
#
# Release opentype-feature-freezer: asks GitHub Actions (.github/workflows/release.yml) to
# create the tag, build, cut a GitHub release, then publish to PyPI through
# Trusted Publishing. No PyPI token is needed locally.
#
# Usage: ./publish.sh            # next patch after the latest vX.Y.Z tag
#        ./publish.sh v1.4.0     # explicit tag
# The tag is made on the HEAD of the remote default branch, so push first.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
BRANCH="$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name)"
git fetch -q --tags origin

TAG="${1:-}"
if [[ -z "$TAG" ]]; then
  last="$(git tag -l 'v[0-9]*.[0-9]*.[0-9]*' --sort=-v:refname | head -n1)"
  IFS=. read -r major minor patch <<<"${last#v}"
  TAG="v${major:-0}.${minor:-0}.$((${patch:-0} + 1))"
fi
if [[ ! "$TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "error: '$TAG' is not a vMAJOR.MINOR.PATCH tag" >&2
  exit 1
fi

if [[ "$(git rev-parse HEAD)" != "$(git rev-parse "origin/$BRANCH")" ]]; then
  echo "warning: local HEAD differs from origin/$BRANCH; the release is cut from origin/$BRANCH" >&2
fi

echo "Releasing $REPO $TAG from $BRANCH"
gh workflow run release.yml -R "$REPO" --ref "$BRANCH" -f tag="$TAG"
sleep 5
gh run list -R "$REPO" --workflow release.yml -L 1
echo "Follow it with: gh run watch -R $REPO"
