#!/bin/bash
# Example script to run Python detection

# Activate virtual environment
source venv/bin/activate

# Run YOLOv8 detector on webcam
python3 src/python/yolov8_detector.py \
    --model models/best.pt \
    --source 0 \
    --confidence 0.5

# Alternative: Run OpenCV detector
# python3 src/python/detector.py \
#     --model models/model.onnx \
#     --source 0 \
#     --confidence 0.5

# Run on video file
# python3 src/python/yolov8_detector.py \
#     --model models/best.pt \
#     --source path/to/video.mp4 \
#     --output output/result.mp4

# Run on image
# python3 src/python/yolov8_detector.py \
#     --model models/best.pt \
#     --source path/to/image.jpg \
#     --output output/result.jpg
