#!/bin/bash
# Setup script for cSUAS Imagery Detection System on Raspberry Pi 5

set -e

echo "==================================="
echo "cSUAS Imagery Setup Script"
echo "==================================="
echo ""

# Check if running on Raspberry Pi
if [ -f /proc/device-tree/model ]; then
    MODEL=$(cat /proc/device-tree/model)
    echo "Detected: $MODEL"
fi

# Update system
echo "Updating system packages..."
sudo apt-get update

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    cmake \
    g++ \
    build-essential \
    libopencv-dev \
    libopencv-contrib-dev \
    git

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "==================================="
echo "Setup complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Run './scripts/setup_submodules.sh' to fetch external repositories"
echo "2. Run './scripts/download_models.sh' to download pre-trained models"
echo "3. Activate the virtual environment: source venv/bin/activate"
echo "4. Build C++ code: mkdir build && cd build && cmake .. && make"
echo ""
