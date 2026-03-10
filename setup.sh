#!/bin/bash

# Sleep Quality Analysis API - Unix Setup Script
# This script automates the setup process for macOS/Linux

set -e

echo ""
echo "==============================================="
echo "Sleep Quality Analysis API - Setup"
echo "==============================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 not found!"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

echo "✓ Python is installed"
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet

# Install requirements
echo ""
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "Error: Failed to install dependencies"
    exit 1
fi

# Create .env file if not exists
echo ""
if [ -f .env ]; then
    echo "✓ .env file already exists"
else
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ .env file created from .env.example"
    else
        echo "Warning: .env.example not found"
    fi
fi

# Check for model file
echo ""
echo "Checking for model file..."
if [ -f "sleep_model.h5" ]; then
    echo "✓ Model file found: sleep_model.h5"
else
    echo "⚠ Warning: sleep_model.h5 not found"
    echo "Please copy your trained model to this directory"
    echo "Expected location: $(pwd)/sleep_model.h5"
fi

# Create required directories
echo ""
echo "Creating required directories..."
mkdir -p models uploads logs
echo "✓ Directories created"

# Setup complete
echo ""
echo "==============================================="
echo "✓ Setup Complete!"
echo "==============================================="
echo ""
echo "To start the server, run:"
echo "  python main.py"
echo ""
echo "Then visit in your browser:"
echo "  http://localhost:8000/docs"
echo ""
echo "Don't forget to activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
