# Scripts

This directory contains automation scripts for maintaining the Homebrew tap.

## update-formulas.py (Full Featured)

A Python script to manually check for and update package versions in the Homebrew formulas. Uses external dependencies for enhanced functionality.

### Requirements

The script will automatically check for dependencies and prompt you to install them if missing.

**Option 1: Install from requirements.txt (recommended)**

```bash
pip3 install -r scripts/requirements.txt
```

**Option 2: Install manually**

```bash
pip3 install requests packaging
```

**Option 3: Using pip (if pip3 isn't available)**

```bash
pip install requests packaging
```

**Option 4: Use the setup script**

```bash
./scripts/setup.sh
```

The script will guide you through installation if dependencies are missing.

### Usage

```bash
# Run from the root of the repository
python3 scripts/update-formulas.py
```

## update-formulas-minimal.py (No Dependencies)

A lightweight version that uses only Python's standard library. Perfect if you don't want to install external dependencies.

### Requirements

None! Uses only Python standard library modules.

### Usage

```bash
# Run from the root of the repository
python3 scripts/update-formulas-minimal.py
```

## setup.sh

A setup script that automatically installs the required dependencies for the full-featured update script.

```bash
./scripts/setup.sh
```

The script will:

1. Check PyPI for the latest versions of your packages
2. Compare with the current versions in the formulas
3. Download and verify new package hashes
4. Update the formula files automatically

### What it updates

- Package version in the download URL
- SHA256 hash of the source archive

## Automated Updates

The repository also includes GitHub Actions workflows for automatic updates:

- **auto-update.yml**: Runs daily to check for new package versions and creates PRs
- **auto-merge.yml**: Automatically merges update PRs after tests pass

These workflows provide a fully automated solution for keeping your Homebrew formulas up to date.
