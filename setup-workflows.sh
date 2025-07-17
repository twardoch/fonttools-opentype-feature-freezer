#!/bin/bash
# this_file: setup-workflows.sh

set -e

echo "🔧 Setting up GitHub Actions workflows..."

# Create .github/workflows directory if it doesn't exist
mkdir -p .github/workflows

# Copy workflow templates
echo "📋 Copying workflow templates..."
cp github-workflows-templates/ci.yml .github/workflows/ci.yml
cp github-workflows-templates/release.yml .github/workflows/release.yml

echo "✅ GitHub Actions workflows have been set up!"
echo ""
echo "📝 Next steps:"
echo "1. Commit and push these workflow files:"
echo "   git add .github/workflows/"
echo "   git commit -m 'Add GitHub Actions workflows'"
echo "   git push"
echo ""
echo "2. Set up required GitHub secrets:"
echo "   - PYPI_API_TOKEN (for PyPI publishing)"
echo "   - CODECOV_TOKEN (optional, for coverage reporting)"
echo ""
echo "3. Test the workflows:"
echo "   - Push to master to trigger CI"
echo "   - Create a git tag (e.g., v1.33.0) to trigger release"
echo ""
echo "For more information, see WORKFLOW_SETUP.md"