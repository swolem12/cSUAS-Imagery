# Troubleshooting Guide

Common issues and solutions for cSUAS-Imagery.

## Installation Issues

### Virtual Environment Creation Fails

**Problem:** `python3 -m venv venv` fails

**Solution:**
```bash
# Install python3-venv
sudo apt-get install python3-venv python3-pip
```

### OpenCV Installation Fails

**Problem:** `pip install opencv-python` fails on Raspberry Pi

**Solution:**
```bash
# Install system dependencies first
sudo apt-get install libopencv-dev python3-opencv

# Or use pre-built wheels
pip install opencv-python-headless
```

### PyTorch Installation Issues

**Problem:** PyTorch installation is very slow or fails on Raspberry Pi

**Solution:**
```bash
# Use lightweight requirements (no PyTorch)
pip install -r requirements-lite.txt

# Or install PyTorch from pre-built wheels
# Visit: https://pytorch.org/get-started/locally/
```

## Model Issues

### Model Not Found

**Problem:** `Model not found at models/best.pt`

**Solution:**
1. Ensure you've run `./scripts/download_models.sh`
2. Check if external repositories are initialized: `./scripts/setup_submodules.sh`
3. Copy or symlink models from external repos:
   ```bash
   ln -s external/Drone-Detection-YOLOv8x/best.pt models/
   ```

### Unsupported Model Format

**Problem:** Model format not supported

**Solution:**
- YOLOv8 `.pt` files: Use `yolov8_detector.py` with ultralytics installed
- ONNX `.onnx` files: Use `detector.py` or C++ detector
- Darknet `.weights`: Need corresponding `.cfg` file
- Convert models to ONNX for best compatibility:
  ```python
  from ultralytics import YOLO
  model = YOLO('model.pt')
  model.export(format='onnx')
  ```

## Camera/Video Issues

### Camera Not Accessible

**Problem:** `Could not open video source`

**Solution:**
```bash
# Add user to video group
sudo usermod -a -G video $USER

# Logout and login again, or:
newgrp video

# Check available cameras
ls -l /dev/video*

# Try different camera indices (0, 1, 2, etc.)
python3 src/python/yolov8_detector.py --model models/best.pt --source 1
```

### Low Frame Rate

**Problem:** Detection is too slow

**Solutions:**
1. Use ONNX models instead of PyTorch
2. Reduce input resolution in config:
   ```yaml
   model:
     input_size: [320, 320]  # Instead of [416, 416]
   ```
3. Increase confidence threshold to reduce processing:
   ```bash
   --confidence 0.7
   ```
4. Use C++ implementation for better performance
5. Disable display window when not needed:
   ```bash
   python3 src/python/yolov8_detector.py --model models/best.pt --source 0 --no-show
   ```

## Build Issues (C++)

### CMake Not Found

**Problem:** `cmake: command not found`

**Solution:**
```bash
sudo apt-get install cmake build-essential
```

### OpenCV Not Found (C++)

**Problem:** CMake can't find OpenCV

**Solution:**
```bash
# Install OpenCV development files
sudo apt-get install libopencv-dev libopencv-contrib-dev

# Check OpenCV installation
pkg-config --modversion opencv4
```

### Build Errors

**Problem:** Compilation errors

**Solution:**
```bash
# Clean and rebuild
make clean
rm -rf build
make build

# Check C++ standard
# Ensure CMakeLists.txt has: set(CMAKE_CXX_STANDARD 17)
```

## Runtime Issues

### Import Errors (Python)

**Problem:** `ModuleNotFoundError: No module named 'ultralytics'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Install missing package
pip install ultralytics

# Or reinstall all dependencies
pip install -r requirements.txt
```

### Segmentation Fault (C++)

**Problem:** Program crashes with segmentation fault

**Solution:**
1. Check model file exists and is not corrupted
2. Verify OpenCV installation
3. Run with debugger:
   ```bash
   gdb ./build/drone_detection
   run --model models/model.onnx --source 0
   ```

### Memory Issues

**Problem:** Out of memory errors

**Solution:**
1. Close other applications
2. Reduce batch size / input resolution
3. Monitor memory usage:
   ```bash
   htop
   ```
4. Increase swap space on Raspberry Pi:
   ```bash
   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile  # Increase CONF_SWAPSIZE
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon
   ```

## Git/Submodule Issues

### Submodules Not Initialized

**Problem:** `external/` directories are empty

**Solution:**
```bash
# Initialize and update submodules
git submodule init
git submodule update --init --recursive

# Or use the script
./scripts/setup_submodules.sh
```

### Submodule Update Fails

**Problem:** `fatal: unable to access` when updating submodules

**Solution:**
```bash
# Check internet connectivity
ping github.com

# Try with HTTPS instead of SSH
git config --global url."https://github.com/".insteadOf git@github.com:

# Update again
git submodule update --init --recursive
```

## Performance Optimization

### Improve Detection Speed

1. **Use ONNX models**: Better CPU performance
2. **Lower resolution**: 320x320 or 416x416
3. **Increase confidence threshold**: Fewer false positives
4. **Use C++ implementation**: Generally faster than Python
5. **Disable visualization**: Don't display video window
6. **Multi-threading**: Configure in `detection_config.yaml`

### Raspberry Pi Specific

```bash
# Overclock (carefully!)
sudo raspi-config
# Performance Options -> Overclock

# Monitor temperature
vcgencmd measure_temp

# Use lightweight desktop or headless mode
sudo systemctl set-default multi-user.target
```

## Still Having Issues?

1. Check system logs: `journalctl -xe`
2. Enable debug mode in Python scripts
3. Run with verbose output
4. Check GitHub issues
5. Open a new issue with:
   - System information
   - Error messages
   - Steps to reproduce
   - Versions of dependencies

## Useful Commands

```bash
# Check Python version
python3 --version

# Check OpenCV version
python3 -c "import cv2; print(cv2.__version__)"

# Check available cameras
v4l2-ctl --list-devices

# Monitor system resources
htop

# Check disk space
df -h

# Check memory
free -h
```
