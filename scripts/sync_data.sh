#!/bin/bash
# Script to sync and manage training data from external repositories

set -e

echo "==================================="
echo "Data Synchronization Script"
echo "==================================="
echo ""

# Create data directories
mkdir -p data/train
mkdir -p data/val
mkdir -p data/test

echo "Checking for datasets in external repositories..."

# Function to copy dataset files
copy_dataset() {
    local source_dir=$1
    local dest_dir=$2
    local file_pattern=$3
    
    if [ -d "$source_dir" ]; then
        echo "Syncing from $source_dir..."
        # Count files to copy
        file_count=$(find "$source_dir" -type f -name "$file_pattern" 2>/dev/null | wc -l)
        
        if [ $file_count -gt 0 ]; then
            echo "  Found $file_count files"
            # Create symlinks to avoid duplicating large files
            find "$source_dir" -type f -name "$file_pattern" -exec ln -sf "$(pwd)/{}" "$dest_dir/" \;
            echo "  Linked to $dest_dir/"
        else
            echo "  No files matching $file_pattern found"
        fi
    else
        echo "  Directory not found: $source_dir"
    fi
}

# Check if submodules are initialized
if [ ! -d "external/seraphim-drone-detection-dataset" ]; then
    echo "Warning: Submodules not initialized."
    echo "Run './scripts/setup_submodules.sh' first."
    exit 1
fi

echo ""
echo "Syncing image datasets..."

# Sync from seraphim dataset
if [ -d "external/seraphim-drone-detection-dataset" ]; then
    echo "Processing seraphim-drone-detection-dataset..."
    copy_dataset "external/seraphim-drone-detection-dataset" "data/train" "*.jpg"
    copy_dataset "external/seraphim-drone-detection-dataset" "data/train" "*.png"
    copy_dataset "external/seraphim-drone-detection-dataset" "data/train" "*.txt"
fi

# Sync from other repositories
if [ -d "external/drone-net/data" ]; then
    echo "Processing drone-net data..."
    copy_dataset "external/drone-net/data" "data/train" "*.jpg"
    copy_dataset "external/drone-net/data" "data/train" "*.png"
fi

if [ -d "external/Drone-Detection-YOLOv8x/data" ]; then
    echo "Processing Drone-Detection-YOLOv8x data..."
    copy_dataset "external/Drone-Detection-YOLOv8x/data" "data/train" "*.jpg"
    copy_dataset "external/Drone-Detection-YOLOv8x/data" "data/train" "*.png"
fi

if [ -d "external/CUAS/dataset" ]; then
    echo "Processing CUAS dataset..."
    copy_dataset "external/CUAS/dataset" "data/train" "*.jpg"
    copy_dataset "external/CUAS/dataset" "data/train" "*.png"
fi

echo ""
echo "==================================="
echo "Data sync complete!"
echo "==================================="
echo ""
echo "Data directories:"
echo "  - data/train: Training data"
echo "  - data/val:   Validation data"
echo "  - data/test:  Test data"
echo ""
echo "Note: Files are symlinked to avoid duplication."
echo "Original files remain in external/ directories."
echo ""
