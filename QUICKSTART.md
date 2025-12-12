# Quick Start Guide

Get up and running with cSUAS-Imagery in 5 minutes.

## Prerequisites

- Raspberry Pi 5 (or Linux system)
- Python 3.8+
- Git

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/swolem12/cSUAS-Imagery.git
cd cSUAS-Imagery

# 2. Setup environment
./scripts/setup_environment.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Initialize external repositories
./scripts/setup_submodules.sh

# 5. Setup models (follow on-screen instructions)
./scripts/download_models.sh
```

## Quick Test

### Python Detection (YOLOv8)

```bash
# Download a YOLOv8 model first
# Place it in models/best.pt

# Run on webcam
python3 src/python/yolov8_detector.py --model models/best.pt --source 0
```

### Python Detection (OpenCV)

```bash
# Use ONNX model
python3 src/python/detector.py --model models/model.onnx --source 0
```

### C++ Detection

```bash
# Build
make build

# Run
./build/drone_detection --model models/model.onnx --source 0
```

## Using Example Scripts

```bash
# Python example
./examples/run_detection_python.sh

# C++ example
./examples/run_detection_cpp.sh
```

## Common Commands

```bash
# Build C++ project
make build

# Clean build artifacts
make clean

# Install Python dependencies
make install

# Run Python detector
make run-python MODEL=models/best.pt

# Run C++ detector
make run-cpp MODEL=models/model.onnx
```

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if you encounter issues
3. Explore configuration options in `config/detection_config.yaml`
4. Review example scripts in `examples/`

## Getting Models

Models can be obtained from:

1. External repositories (in `external/` after running setup_submodules.sh)
2. Download from [Ultralytics](https://github.com/ultralytics/assets/releases)
3. Train your own using datasets from external repositories

## Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [CONTRIBUTING.md](CONTRIBUTING.md)
- Open an issue on GitHub
