#!/bin/bash
# this_file: scripts/release.sh

set -e

if [ $# -eq 0 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.33.0"
    exit 1
fi

VERSION=$1

echo "🚀 Preparing release $VERSION..."

# Check if git is clean
if ! git diff-index --quiet HEAD --; then
    echo "❌ Git working directory is not clean. Please commit or stash changes."
    exit 1
fi

# Check if we're on the right branch
BRANCH=$(git symbolic-ref --short HEAD)
if [ "$BRANCH" != "master" ]; then
    echo "❌ Not on master branch. Please switch to master."
    exit 1
fi

# Update version in changelog
echo "📝 Updating CHANGELOG.md..."
if [ -f "CHANGELOG.md" ]; then
    # Add new version entry to changelog
    DATE=$(date +%Y-%m-%d)
    sed -i.bak "s/## \[Unreleased\]/## [Unreleased]\n\n## [$VERSION] - $DATE/" CHANGELOG.md
    rm CHANGELOG.md.bak
fi

# Run tests
echo "🧪 Running tests..."
./scripts/test.sh

# Build the package
echo "🏗️  Building package..."
./scripts/build.sh

# Create and push git tag
echo "🏷️  Creating git tag..."
git add .
git commit -m "Release v$VERSION" || true  # Allow empty commit
git tag -a "v$VERSION" -m "Release v$VERSION"

echo "📤 Pushing to remote..."
git push origin master
git push origin "v$VERSION"

echo "✅ Release $VERSION completed!"
echo "🚀 GitHub Actions will automatically:"
echo "   - Run tests"
echo "   - Build packages"
echo "   - Create GitHub release"
echo "   - Upload to PyPI"