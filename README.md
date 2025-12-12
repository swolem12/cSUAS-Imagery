# cSUAS-Imagery

Counter-UAS (Unmanned Aerial Systems) Detection System for Raspberry Pi 5

## Overview

This repository provides a comprehensive drone detection system optimized for Raspberry Pi 5, integrating training models and datasets from multiple sources. The system supports both Python and C++ implementations for real-time drone detection using YOLO and OpenCV.

## Features

- **Dual Language Support**: Python and C++ implementations
- **Multiple Model Support**: YOLOv8, YOLOv5, Darknet, ONNX
- **Real-time Detection**: Optimized for Raspberry Pi 5
- **Integrated Datasets**: Pulls from multiple drone detection repositories
- **Flexible Input**: Support for webcam, video files, and images
- **Easy Setup**: Automated scripts for environment and model setup

## Repository Structure

```
cSUAS-Imagery/
├── src/
│   ├── python/           # Python detection modules
│   │   ├── detector.py   # OpenCV-based detector
│   │   └── yolov8_detector.py  # YOLOv8 detector
│   └── cpp/              # C++ detection modules
│       ├── drone_detector.hpp
│       ├── drone_detector.cpp
│       └── main.cpp
├── external/             # Git submodules (initialized via setup)
│   ├── drone-net/
│   ├── Drone-Detection-YOLOv8x/
│   ├── seraphim-drone-detection-dataset/
│   └── CUAS/
├── models/               # Model files (downloaded separately)
├── data/                 # Training/testing data
├── config/               # Configuration files
│   └── detection_config.yaml
├── scripts/              # Setup and utility scripts
│   ├── setup_environment.sh
│   ├── setup_submodules.sh
│   └── download_models.sh
├── examples/             # Example usage scripts
├── requirements.txt      # Python dependencies
└── CMakeLists.txt        # C++ build configuration
```

## External Repositories

This project integrates models and datasets from:

1. **[drone-net](https://github.com/swolem12/drone-net)** - Neural network models for drone detection
2. **[Drone-Detection-YOLOv8x](https://github.com/swolem12/Drone-Detection-YOLOv8x)** - YOLOv8x trained models
3. **[seraphim-drone-detection-dataset](https://github.com/swolem12/seraphim-drone-detection-dataset)** - Training datasets
4. **[CUAS](https://github.com/cweekiat/CUAS)** - Counter-UAS research materials

## Installation

### Prerequisites

- Raspberry Pi 5 (or compatible Linux system)
- Python 3.8+
- CMake 3.10+
- OpenCV 4.8+
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/swolem12/cSUAS-Imagery.git
cd cSUAS-Imagery
```

2. **Setup environment and dependencies**
```bash
./scripts/setup_environment.sh
```

3. **Initialize submodules (pull external repositories)**
```bash
./scripts/setup_submodules.sh
```

4. **Setup models**
```bash
./scripts/download_models.sh
```

5. **Activate virtual environment**
```bash
source venv/bin/activate
```

## Usage

### Python Detection

#### Using YOLOv8
```bash
# Webcam detection
python3 src/python/yolov8_detector.py --model models/best.pt --source 0

# Video file detection
python3 src/python/yolov8_detector.py --model models/best.pt --source video.mp4 --output result.mp4

# Image detection
python3 src/python/yolov8_detector.py --model models/best.pt --source image.jpg
```

#### Using OpenCV DNN
```bash
python3 src/python/detector.py --model models/model.onnx --source 0 --confidence 0.5
```

### C++ Detection

1. **Build the project**
```bash
mkdir build && cd build
cmake ..
make
cd ..
```

2. **Run detection**
```bash
# Webcam detection
./build/drone_detection --model models/model.onnx --source 0

# Video file detection
./build/drone_detection --model models/model.onnx --source video.mp4 --output result.mp4

# With Darknet models
./build/drone_detection --model models/yolo.weights --config models/yolo.cfg --source 0
```

### Example Scripts

Pre-configured example scripts are available in the `examples/` directory:

```bash
# Python example
./examples/run_detection_python.sh

# C++ example
./examples/run_detection_cpp.sh
```

## Configuration

Edit `config/detection_config.yaml` to customize detection parameters:

- Model paths and types
- Confidence and NMS thresholds
- Video source settings
- Output options
- Raspberry Pi optimizations
- Alert settings

## Model Management

### Supported Model Formats

- **YOLOv8**: `.pt` files (requires ultralytics)
- **ONNX**: `.onnx` files (OpenCV DNN)
- **Darknet**: `.weights` + `.cfg` files
- **TensorFlow**: `.pb`, `.h5` files

### Adding Models

1. Copy model files to the `models/` directory
2. Update the configuration file or command-line arguments
3. For models from external repositories, use symlinks:
```bash
ln -s external/Drone-Detection-YOLOv8x/best.pt models/
```

## Raspberry Pi 5 Optimization

The system is optimized for Raspberry Pi 5:

- CPU-optimized OpenCV DNN backend
- Configurable thread count
- Efficient memory management
- Lower resolution processing options

### Performance Tips

1. Use ONNX models for better CPU performance
2. Reduce input resolution (e.g., 416x416 instead of 640x640)
3. Adjust confidence threshold based on use case
4. Enable multi-threading in configuration

## Development

### Adding New Detectors

1. For Python: Create a new module in `src/python/`
2. For C++: Add source files to `src/cpp/` and update `CMakeLists.txt`
3. Follow the existing detector interface pattern

### Testing

```bash
# Python tests (if available)
pytest tests/

# C++ tests
cd build && ctest
```

## Troubleshooting

### Common Issues

1. **Model not found**: Ensure models are downloaded and paths are correct
2. **Camera not accessible**: Check permissions (`sudo usermod -a -G video $USER`)
3. **Low FPS**: Reduce input resolution or use ONNX models
4. **Import errors**: Activate virtual environment (`source venv/bin/activate`)

### Performance Issues

- Check CPU/GPU utilization
- Monitor memory usage
- Adjust detection parameters in config
- Consider using lightweight models

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project integrates code and models from multiple sources. Please check individual repositories for their respective licenses:

- [drone-net](https://github.com/swolem12/drone-net)
- [Drone-Detection-YOLOv8x](https://github.com/swolem12/Drone-Detection-YOLOv8x)
- [seraphim-drone-detection-dataset](https://github.com/swolem12/seraphim-drone-detection-dataset)
- [CUAS](https://github.com/cweekiat/CUAS)

## Acknowledgments

This project builds upon work from:
- swolem12 (drone-net, Drone-Detection-YOLOv8x, seraphim-drone-detection-dataset)
- cweekiat (CUAS)
- Ultralytics (YOLOv8)
- OpenCV community

## Contact

For issues and questions, please open an issue on GitHub.

## References

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [OpenCV DNN Module](https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html)
- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
