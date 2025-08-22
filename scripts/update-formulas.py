#!/usr/bin/env python3
"""
Manual formula updater script for clxrityy/homebrew-tap

This script checks for updates to your Python packages and updates the Homebrew formulas accordingly.
"""

import re
import hashlib
import sys
import os
from pathlib import Path

# Check for required dependencies
def check_dependencies():
    """Check if required packages are available and install if needed."""
    missing_packages = []
    
    try:
        import requests
    except ImportError:
        missing_packages.append("requests")
    
    try:
        from packaging import version
    except ImportError:
        missing_packages.append("packaging")
    
    if missing_packages:
        print("❌ Missing required dependencies:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 To install dependencies, run:")
        print(f"   pip3 install {' '.join(missing_packages)}")
        print("\n   Or if you prefer using pip:")
        print(f"   pip install {' '.join(missing_packages)}")
        sys.exit(1)

# Check dependencies before importing
check_dependencies()

import requests
from packaging import version

PACKAGES = [
    {
        "name": "autochange",
        "pypi_name": "autochange",
        "formula_path": "Formula/autochange.rb"
    },
    {
        "name": "gatenet",
        "pypi_name": "gatenet", 
        "formula_path": "Formula/gatenet.rb"
    }
]

def get_latest_version(package_name):
    """Get the latest version from PyPI."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=30)
        response.raise_for_status()
        return response.json()["info"]["version"]
    except Exception as e:
        print(f"Error fetching version for {package_name}: {e}")
        return None

def get_current_version(formula_path):
    """Extract current version from formula file."""
    try:
        with open(formula_path, 'r') as f:
            content = f.read()
        
        version_match = re.search(r'url\s+"[^"]*-(\d+\.\d+\.\d+)\.tar\.gz"', content)
        if version_match:
            return version_match.group(1)
        return None
    except Exception as e:
        print(f"Error reading formula {formula_path}: {e}")
        return None

def calculate_sha256(url):
    """Download file and calculate SHA256 hash."""
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        return hashlib.sha256(response.content).hexdigest()
    except Exception as e:
        print(f"Error downloading/hashing {url}: {e}")
        return None

def update_formula(formula_path, package_name, current_version, new_version, new_sha256):
    """Update the formula file with new version and hash."""
    try:
        with open(formula_path, 'r') as f:
            content = f.read()
        
        # Update URL
        old_url_pattern = rf'url\s+"[^"]*{re.escape(package_name)}-{re.escape(current_version)}\.tar\.gz"'
        new_url = f'url "https://pypi.org/packages/source/{package_name[0]}/{package_name}/{package_name}-{new_version}.tar.gz"'
        content = re.sub(old_url_pattern, f'  {new_url}', content)
        
        # Update SHA256
        sha256_pattern = r'sha256\s+"[a-f0-9]{64}"'
        new_sha256_line = f'sha256 "{new_sha256}"'
        content = re.sub(sha256_pattern, f'  {new_sha256_line}', content)
        
        with open(formula_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {formula_path}")
        return True
    except Exception as e:
        print(f"❌ Error updating {formula_path}: {e}")
        return False

def process_package_update(package, current_version, latest_version):
    """Process the update for a single package."""
    print("   🔄 Update available!")
    
    # Calculate new hash
    source_url = f"https://pypi.org/packages/source/{package['pypi_name'][0]}/{package['pypi_name']}/{package['pypi_name']}-{latest_version}.tar.gz"
    print(f"   📥 Downloading {source_url}...")
    
    new_sha256 = calculate_sha256(source_url)
    if not new_sha256:
        print(f"   ❌ Failed to calculate hash for {package['name']}")
        return False
    
    print(f"   🔐 SHA256: {new_sha256}")
    
    # Update formula
    if update_formula(package['formula_path'], package['pypi_name'], current_version, latest_version, new_sha256):
        print(f"   ✅ {package['name']} updated to {latest_version}")
        return True
    else:
        print(f"   ❌ Failed to update {package['name']}")
        return False

def check_package_versions(package):
    """Check current and latest versions for a package."""
    current_version = get_current_version(package['formula_path'])
    if not current_version:
        print(f"❌ Could not determine current version for {package['name']}")
        return None, None
        
    latest_version = get_latest_version(package['pypi_name'])
    if not latest_version:
        print(f"❌ Could not fetch latest version for {package['name']}")
        return None, None
    
    return current_version, latest_version

def main():
    """Main function to check and update all packages."""
    print("🔍 Checking for package updates...\n")
    
    # Change to the script's directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    updates_available = False
    
    for package in PACKAGES:
        print(f"Checking {package['name']}...")
        
        current_version, latest_version = check_package_versions(package)
        if not current_version or not latest_version:
            continue
        
        print(f"   Current: {current_version}")
        print(f"   Latest:  {latest_version}")
        
        # Compare versions
        if version.parse(latest_version) > version.parse(current_version):
            if process_package_update(package, current_version, latest_version):
                updates_available = True
        else:
            print("   ✅ Up to date")
        
        print()
    
    if updates_available:
        print("🎉 Updates completed! Don't forget to:")
        print("   1. Test the updated formulas with 'brew style' and 'brew audit'")
        print("   2. Commit and push your changes")
        print("   3. The GitHub Actions will run tests automatically")
    else:
        print("✅ All packages are up to date!")

if __name__ == "__main__":
    main()
