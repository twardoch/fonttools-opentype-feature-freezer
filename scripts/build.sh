#!/bin/bash
# this_file: scripts/build.sh

set -e

echo "🔧 Building OpenType Feature Freezer..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ src/opentype_feature_freezer/_version.py

# Install/upgrade build dependencies
echo "📦 Installing build dependencies..."
python3 -m pip install --upgrade pip build hatch

# Build the package
echo "🏗️  Building package..."
python3 -m build

# Build GUI executables if PyInstaller is available
if command -v pyinstaller &> /dev/null; then
    echo "🖥️  Building GUI executables..."
    cd app
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        pyinstaller --clean pyinstaller-mac.spec
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        pyinstaller --clean pyinstaller-win.spec
    else
        echo "ℹ️  GUI build not configured for this platform"
    fi
    cd ..
else
    echo "ℹ️  PyInstaller not found, skipping GUI build"
fi

echo "✅ Build completed successfully!"
echo "📦 Distribution files are in: dist/"
ls -la dist/