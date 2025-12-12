#!/bin/bash
# Script to validate cSUAS-Imagery installation

echo "==================================="
echo "cSUAS-Imagery Setup Validator"
echo "==================================="
echo ""

ERRORS=0
WARNINGS=0

# Function to check command
check_command() {
    if command -v "$1" &> /dev/null; then
        echo "✓ $1 is installed"
        if [ -n "$2" ]; then
            VERSION=$($1 $2 2>&1 | head -1)
            echo "  Version: $VERSION"
        fi
        return 0
    else
        echo "✗ $1 is NOT installed"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

# Check system commands
echo "Checking system commands..."
check_command "python3" "--version"
check_command "pip3" "--version"
check_command "git" "--version"
check_command "cmake" "--version"
check_command "g++" "--version"
echo ""

# Check Python packages
echo "Checking Python packages..."
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment found"
else
    echo "⚠ Virtual environment not found"
    WARNINGS=$((WARNINGS + 1))
fi

# Check required Python packages
python3 -c "import cv2" 2>/dev/null && echo "✓ OpenCV is installed" || { echo "✗ OpenCV is NOT installed"; ERRORS=$((ERRORS + 1)); }
python3 -c "import numpy" 2>/dev/null && echo "✓ NumPy is installed" || { echo "✗ NumPy is NOT installed"; ERRORS=$((ERRORS + 1)); }
python3 -c "import yaml" 2>/dev/null && echo "✓ PyYAML is installed" || { echo "✗ PyYAML is NOT installed"; ERRORS=$((ERRORS + 1)); }

# Check optional packages
python3 -c "import ultralytics" 2>/dev/null && echo "✓ Ultralytics is installed" || { echo "⚠ Ultralytics is NOT installed (YOLOv8 support disabled)"; WARNINGS=$((WARNINGS + 1)); }
python3 -c "import torch" 2>/dev/null && echo "✓ PyTorch is installed" || { echo "⚠ PyTorch is NOT installed (YOLOv8 support disabled)"; WARNINGS=$((WARNINGS + 1)); }
echo ""

# Check directories
echo "Checking directory structure..."
for dir in src models data config scripts examples; do
    if [ -d "$dir" ]; then
        echo "✓ $dir/ directory exists"
    else
        echo "✗ $dir/ directory is missing"
        ERRORS=$((ERRORS + 1))
    fi
done
echo ""

# Check submodules
echo "Checking Git submodules..."
if [ -d "external/drone-net" ]; then
    echo "✓ drone-net submodule initialized"
else
    echo "⚠ drone-net submodule not initialized"
    WARNINGS=$((WARNINGS + 1))
fi

if [ -d "external/Drone-Detection-YOLOv8x" ]; then
    echo "✓ Drone-Detection-YOLOv8x submodule initialized"
else
    echo "⚠ Drone-Detection-YOLOv8x submodule not initialized"
    WARNINGS=$((WARNINGS + 1))
fi

if [ -d "external/seraphim-drone-detection-dataset" ]; then
    echo "✓ seraphim-drone-detection-dataset submodule initialized"
else
    echo "⚠ seraphim-drone-detection-dataset submodule not initialized"
    WARNINGS=$((WARNINGS + 1))
fi

if [ -d "external/CUAS" ]; then
    echo "✓ CUAS submodule initialized"
else
    echo "⚠ CUAS submodule not initialized"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Check models
echo "Checking for models..."
MODEL_COUNT=$(find models -type f \( -name "*.pt" -o -name "*.onnx" -o -name "*.weights" -o -name "*.h5" \) 2>/dev/null | wc -l)
if [ $MODEL_COUNT -gt 0 ]; then
    echo "✓ Found $MODEL_COUNT model file(s)"
    find models -type f \( -name "*.pt" -o -name "*.onnx" -o -name "*.weights" -o -name "*.h5" \) -exec echo "  - {}" \;
else
    echo "⚠ No model files found in models/ directory"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Check C++ build
echo "Checking C++ build..."
if [ -d "build" ]; then
    if [ -f "build/drone_detection" ]; then
        echo "✓ C++ executable is built"
    else
        echo "⚠ C++ executable not found (run 'make build')"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo "⚠ Build directory not found (run 'make build')"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Summary
echo "==================================="
echo "Validation Summary"
echo "==================================="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✓ All checks passed! Your setup is complete."
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠ Setup is functional but some optional components are missing."
    echo "Run the following to complete setup:"
    [ ! -d "venv" ] && echo "  - ./scripts/setup_environment.sh"
    [ ! -d "external/drone-net" ] && echo "  - ./scripts/setup_submodules.sh"
    [ $MODEL_COUNT -eq 0 ] && echo "  - ./scripts/download_models.sh"
    [ ! -f "build/drone_detection" ] && echo "  - make build"
    exit 0
else
    echo "✗ Setup has errors that need to be fixed."
    echo "Please resolve the errors above and run this script again."
    exit 1
fi
