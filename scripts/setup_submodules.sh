#!/bin/bash
# Script to initialize and update all Git submodules

set -e

echo "Initializing Git submodules..."
git submodule init

echo "Updating submodules..."
git submodule update --init --recursive

echo "Submodules setup complete!"
echo ""
echo "Available submodules:"
echo "  - external/drone-net"
echo "  - external/Drone-Detection-YOLOv8x"
echo "  - external/seraphim-drone-detection-dataset"
echo "  - external/CUAS"
