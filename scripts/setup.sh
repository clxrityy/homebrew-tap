#!/bin/bash
# Setup script for update-formulas.py dependencies

echo "🔧 Setting up dependencies for update-formulas.py..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found. Please install Python 3 first."
    exit 1
fi

# Try to install dependencies
if pip3 install -r scripts/requirements.txt; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "You can now run the update script:"
    echo "   python3 scripts/update-formulas.py"
elif pip install -r scripts/requirements.txt; then
    echo "✅ Dependencies installed successfully with pip!"
    echo ""
    echo "You can now run the update script:"
    echo "   python3 scripts/update-formulas.py"
else
    echo "❌ Failed to install dependencies. Please try manually:"
    echo "   pip3 install requests packaging"
    echo "   OR"
    echo "   pip install requests packaging"
    exit 1
fi
