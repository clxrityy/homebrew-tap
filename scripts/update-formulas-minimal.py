#!/usr/bin/env python3
"""
Lightweight formula updater using only Python standard library.

This is a minimal version that uses urllib instead of requests.
For the full-featured version, use update-formulas.py
"""

import urllib.request
import json
import re
import hashlib
import os
from pathlib import Path

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

def compare_versions(v1, v2):
    """Basic version comparison (works for simple semantic versions)."""
    v1_parts = list(map(int, v1.split('.')))
    v2_parts = list(map(int, v2.split('.')))
    
    # Pad with zeros if needed
    while len(v1_parts) < len(v2_parts):
        v1_parts.append(0)
    while len(v2_parts) < len(v1_parts):
        v2_parts.append(0)
    
    return v1_parts < v2_parts

def get_latest_version(package_name):
    """Get the latest version from PyPI using urllib."""
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data["info"]["version"]
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
    """Download file and calculate SHA256 hash using urllib."""
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            return hashlib.sha256(response.read()).hexdigest()
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

def process_package(package):
    """Process a single package for updates."""
    print(f"Checking {package['name']}...")
    
    # Get versions
    current_version = get_current_version(package['formula_path'])
    if not current_version:
        print(f"❌ Could not determine current version for {package['name']}")
        return False
        
    latest_version = get_latest_version(package['pypi_name'])
    if not latest_version:
        print(f"❌ Could not fetch latest version for {package['name']}")
        return False
    
    print(f"   Current: {current_version}")
    print(f"   Latest:  {latest_version}")
    
    # Compare versions
    if compare_versions(current_version, latest_version):
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
    else:
        print("   ✅ Up to date")
        return False

def main():
    """Main function to check and update all packages."""
    print("🔍 Checking for package updates (stdlib version)...\n")
    
    # Change to the script's directory parent (repository root)
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    updates_available = False
    
    for package in PACKAGES:
        if process_package(package):
            updates_available = True
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
