# GitHub Actions Workflow Setup

Due to GitHub App permissions, the workflow files need to be manually activated after committing the changes.

## Setup Instructions

1. **After committing these changes**, manually rename the workflow files:

```bash
# Navigate to your repository
cd .github/workflows/

# Rename the example files to activate them
mv ci.yml.example ci.yml
mv release.yml.example release.yml

# Commit the activated workflows
git add ci.yml release.yml
git commit -m "Activate GitHub Actions workflows

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

2. **Set up GitHub Secrets** (required for full functionality):

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- `PYPI_API_TOKEN`: Your PyPI API token for publishing packages
- `CODECOV_TOKEN`: (Optional) Codecov token for coverage reporting

## What the Workflows Do

### CI Workflow (`ci.yml`)
- **Triggers**: Push to master, Pull requests
- **Tests**: Python 3.8-3.12 on Ubuntu, Windows, macOS
- **Checks**: Linting, type checking, tests with coverage
- **Builds**: Python packages and GUI executables

### Release Workflow (`release.yml`)
- **Triggers**: Git tags starting with `v` (e.g., `v1.33.0`)
- **Actions**: 
  - Runs full test suite
  - Builds Python packages
  - Creates GUI executables for Windows and macOS
  - Creates GitHub release with downloadable assets
  - Publishes to PyPI automatically

## Testing the Setup

1. **Test CI**: Create a pull request or push to master
2. **Test Release**: Create and push a git tag:
   ```bash
   git tag -a v1.33.0 -m "Release v1.33.0"
   git push origin v1.33.0
   ```

## Alternative: Manual Workflow Creation

If you prefer to create the workflows manually:

1. Create `.github/workflows/ci.yml` with the content from `ci.yml.example`
2. Create `.github/workflows/release.yml` with the content from `release.yml.example`
3. Commit and push these files

## Troubleshooting

- **Permission errors**: Ensure you have admin access to the repository
- **Workflow not running**: Check that the files are named correctly (`.yml` not `.yml.example`)
- **Build failures**: Ensure all secrets are set up correctly
- **PyPI publishing fails**: Verify `PYPI_API_TOKEN` is valid and has publishing permissions

---

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>