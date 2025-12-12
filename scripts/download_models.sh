#!/bin/bash
# Script to download pre-trained models from external repositories

set -e

echo "==================================="
echo "Model Download Script"
echo "==================================="
echo ""

# Create models directory if it doesn't exist
mkdir -p models

echo "This script will help you set up models from the external repositories."
echo ""
echo "Available model sources:"
echo "  1. drone-net (external/drone-net)"
echo "  2. Drone-Detection-YOLOv8x (external/Drone-Detection-YOLOv8x)"
echo "  3. seraphim-drone-detection-dataset (external/seraphim-drone-detection-dataset)"
echo "  4. CUAS (external/CUAS)"
echo ""

# Function to check if submodules are initialized
check_submodules() {
    if [ ! -d "external/drone-net" ] || [ ! -d "external/Drone-Detection-YOLOv8x" ]; then
        echo "Warning: Submodules not initialized."
        echo "Run './scripts/setup_submodules.sh' first."
        exit 1
    fi
}

# Check submodules
check_submodules

echo "Looking for models in external repositories..."

# Search for model files in submodules
if [ -d "external/drone-net" ]; then
    echo "Checking drone-net..."
    find external/drone-net -type f \( -name "*.weights" -o -name "*.pt" -o -name "*.onnx" -o -name "*.h5" \) -exec echo "  Found: {}" \;
fi

if [ -d "external/Drone-Detection-YOLOv8x" ]; then
    echo "Checking Drone-Detection-YOLOv8x..."
    find external/Drone-Detection-YOLOv8x -type f \( -name "*.weights" -o -name "*.pt" -o -name "*.onnx" -o -name "*.h5" \) -exec echo "  Found: {}" \;
fi

if [ -d "external/CUAS" ]; then
    echo "Checking CUAS..."
    find external/CUAS -type f \( -name "*.weights" -o -name "*.pt" -o -name "*.onnx" -o -name "*.h5" \) -exec echo "  Found: {}" \;
fi

echo ""
echo "==================================="
echo "Model Setup Instructions"
echo "==================================="
echo ""
echo "To use models from external repositories:"
echo "1. Copy or symlink model files to the 'models/' directory"
echo "2. Example: ln -s ../external/drone-net/model.pt models/"
echo "3. Or: cp external/Drone-Detection-YOLOv8x/best.pt models/"
echo ""
echo "You can also download models from:"
echo "  - YOLOv8: https://github.com/ultralytics/assets/releases"
echo "  - Custom trained models from the external repositories"
echo ""
