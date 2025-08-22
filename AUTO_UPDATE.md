# Automated Formula Updates

This repository now includes a comprehensive automated update system for keeping your Homebrew formulas up to date with the latest package releases.

## 🤖 How It Works

### 1. Daily Automatic Checks

- **Schedule**: Every day at 6 AM UTC
- **Process**: GitHub Actions checks PyPI for new versions of your packages
- **Smart Detection**: Only creates PRs when actual updates are available

### 2. Automated Testing

When an update is found, the system automatically:

- ✅ Downloads the new package and calculates SHA256 hash
- ✅ Updates the formula file with new version and hash
- ✅ Runs `brew style` to check coding standards
- ✅ Runs `brew audit` to validate the formula
- ✅ Tests installation of the updated package
- ✅ Runs the formula's test suite

### 3. Pull Request Creation

- 📝 Creates a detailed PR with version changes
- 🏷️ Adds appropriate labels (`automated-update`, `dependencies`)
- 📊 Includes test results and validation status

### 4. Automatic Merging (Optional)

- ⏱️ Waits for all CI tests to complete
- ✅ Auto-merges if all tests pass
- 🚫 Leaves PR open for manual review if tests fail

## 📁 Files Added

### GitHub Actions Workflows

- `.github/workflows/auto-update.yml` - Main update workflow
- `.github/workflows/auto-merge.yml` - Auto-merge workflow

### Manual Scripts

- `scripts/update-formulas.py` - Manual update script
- `scripts/README.md` - Documentation for scripts

## 🚀 Getting Started

### Option 1: Fully Automated (Recommended)

1. The workflows are already configured and will run automatically
2. PRs will be created when updates are available
3. If auto-merge is enabled, they'll merge automatically after tests pass

### Option 2: Manual Control

If you prefer manual control:

1. Disable auto-merge by removing the `auto-merge.yml` workflow
2. Review and merge update PRs manually
3. Or use the manual script: `python3 scripts/update-formulas.py`
   - For dependency-free operation: `python3 scripts/update-formulas-minimal.py`

## ⚙️ Configuration

### Packages Monitored

The system currently monitors:

- **autochange** (`autochange` on PyPI)
- **gatenet** (`gatenet` on PyPI)

### Adding New Packages

To monitor additional packages, edit the `matrix.package` section in `.github/workflows/auto-update.yml`:

```yaml
matrix:
  package:
    - name: your-package-name
      pypi_name: your-pypi-package-name
      formula_path: Formula/your-package.rb
```

### Scheduling

The update check runs daily at 6 AM UTC. To change this, modify the cron schedule in `auto-update.yml`:

```yaml
on:
  schedule:
    - cron: "0 6 * * *" # Change this line
```

## 🔧 Manual Updates

If you need to manually check for updates:

**Option 1: Full-featured script (with dependencies)**

```bash
# Install dependencies (one-time setup)
pip3 install -r scripts/requirements.txt
# OR use the setup script
./scripts/setup.sh

# Run the update script
python3 scripts/update-formulas.py
```

**Option 2: Minimal script (no dependencies required)**

```bash
# No setup needed - uses only Python standard library
python3 scripts/update-formulas-minimal.py
```

## 🛡️ Security

- Updates are only applied for packages you own/control
- All changes go through PR review process
- Full test suite runs before any merging
- Source verification with SHA256 hashes

## 🎯 Benefits

- ⚡ **Fast**: Updates appear within 24 hours of release
- 🔒 **Safe**: Full testing before any changes are merged
- 📈 **Reliable**: No more manual version tracking
- 🔄 **Consistent**: Standardized update process
- 👀 **Transparent**: All changes visible in PR history

Your Homebrew tap will now stay automatically synchronized with your latest package releases! 🎉
