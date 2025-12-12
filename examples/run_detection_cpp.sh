#!/bin/bash
# Example script to build and run C++ detection

# Build the project
echo "Building C++ detection system..."
mkdir -p build
cd build
cmake ..
make
cd ..

# Run detector on webcam
./build/drone_detection \
    --model models/model.onnx \
    --source 0 \
    --confidence 0.5

# Alternative: Run on video file
# ./build/drone_detection \
#     --model models/model.onnx \
#     --source path/to/video.mp4 \
#     --output output/result.mp4

# For Darknet models with config
# ./build/drone_detection \
#     --model models/yolo.weights \
#     --config models/yolo.cfg \
#     --source 0
