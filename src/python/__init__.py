"""
cSUAS-Imagery Detection Package
Drone detection system for Raspberry Pi 5
"""

__version__ = "1.0.0"
__author__ = "cSUAS-Imagery Contributors"

from .detector import DroneDetector

try:
    from .yolov8_detector import YOLOv8DroneDetector
except ImportError:
    # ultralytics not installed
    YOLOv8DroneDetector = None

from .config_loader import ConfigLoader

__all__ = [
    'DroneDetector',
    'YOLOv8DroneDetector',
    'ConfigLoader',
]
