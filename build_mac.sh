#!/bin/bash
# Obscura - macOS Build Script
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.

set -e  # Exit on error

echo "========================================"
echo "  Obscura - macOS Build Script"
echo "========================================"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Python version: $PYTHON_VERSION"

if [[ $(echo "$PYTHON_VERSION < 3.11" | bc -l) -eq 1 ]]; then
    echo "Error: Python 3.11 or higher is required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# Build the application
echo ""
echo "Building Obscura..."
pyinstaller --name "Obscura" \
    --windowed \
    --onefile \
    --icon=obscura_icon.png \
    --add-data "core:core" \
    --add-data "windows_app:windows_app" \
    run.py

echo ""
echo "========================================"
echo "  Build Complete!"
echo "========================================"
echo ""
echo "Output: dist/Obscura"
echo ""
echo "To run: ./dist/Obscura"
echo ""
