#!/usr/bin/env python3
"""
YOLOv8-based Drone Detection System for Raspberry Pi 5
Uses the ultralytics library for YOLOv8 models
"""

import argparse
from pathlib import Path
from typing import Optional
import cv2

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False
    print("Warning: ultralytics not installed. Install with: pip install ultralytics")


class YOLOv8DroneDetector:
    """Drone detector using YOLOv8 models"""
    
    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        """
        Initialize YOLOv8 detector
        
        Args:
            model_path: Path to YOLOv8 model (.pt file)
            confidence_threshold: Minimum confidence for detections
        """
        if not ULTRALYTICS_AVAILABLE:
            raise ImportError("ultralytics package is required. Install with: pip install ultralytics")
        
        self.model_path = Path(model_path)
        self.confidence_threshold = confidence_threshold
        self.model = None
        
        self._load_model()
    
    def _load_model(self):
        """Load the YOLOv8 model"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        print(f"Loading YOLOv8 model from {self.model_path}...")
        self.model = YOLO(str(self.model_path))
        print("Model loaded successfully")
    
    def detect_video(self, source: str = "0", output_path: Optional[str] = None, 
                     show: bool = True):
        """
        Run detection on video source
        
        Args:
            source: Video source (0 for webcam, or path to video)
            output_path: Path to save output video (optional)
            show: Whether to display the video
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        # Convert source to int if it's a digit
        if isinstance(source, str) and source.isdigit():
            source = int(source)
        
        # Open video source
        cap = cv2.VideoCapture(source)
        
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video source: {source}")
        
        # Setup video writer if output specified
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        print("Starting detection... Press 'q' to quit")
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Run detection
                results = self.model(frame, conf=self.confidence_threshold, verbose=False)
                
                # Draw results on frame
                annotated_frame = results[0].plot()
                
                # Add detection count
                detections = results[0].boxes
                count = len(detections) if detections is not None else 0
                cv2.putText(annotated_frame, f"Drones: {count}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Write to output if specified
                if writer:
                    writer.write(annotated_frame)
                
                # Show frame
                if show:
                    cv2.imshow('YOLOv8 Drone Detection', annotated_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        
        finally:
            # Cleanup
            cap.release()
            if writer:
                writer.release()
            if show:
                cv2.destroyAllWindows()
            print("Detection stopped")
    
    def detect_image(self, image_path: str, output_path: Optional[str] = None,
                     show: bool = True):
        """
        Run detection on a single image
        
        Args:
            image_path: Path to input image
            output_path: Path to save output image (optional)
            show: Whether to display the image
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        # Run detection
        results = self.model(image_path, conf=self.confidence_threshold)
        
        # Get annotated image
        annotated_image = results[0].plot()
        
        # Save if output path specified
        if output_path:
            cv2.imwrite(output_path, annotated_image)
            print(f"Output saved to {output_path}")
        
        # Show image
        if show:
            cv2.imshow('YOLOv8 Drone Detection', annotated_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        # Print detection info
        detections = results[0].boxes
        count = len(detections) if detections is not None else 0
        print(f"Detected {count} drone(s)")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='YOLOv8 Drone Detection System')
    parser.add_argument('--model', type=str, required=True, 
                       help='Path to YOLOv8 model file (.pt)')
    parser.add_argument('--source', type=str, default='0',
                       help='Video source (0 for webcam, path to video, or path to image)')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='Confidence threshold (0-1)')
    parser.add_argument('--output', type=str,
                       help='Output file path (optional)')
    parser.add_argument('--no-show', action='store_true',
                       help='Do not display output')
    
    args = parser.parse_args()
    
    if not ULTRALYTICS_AVAILABLE:
        print("Error: ultralytics package not installed")
        print("Install with: pip install ultralytics")
        return
    
    # Initialize detector
    detector = YOLOv8DroneDetector(args.model, args.confidence)
    
    # Check if source is an image or video
    source_path = Path(args.source)
    if source_path.exists() and source_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
        # Image detection
        detector.detect_image(args.source, args.output, not args.no_show)
    else:
        # Video detection
        detector.detect_video(args.source, args.output, not args.no_show)


if __name__ == '__main__':
    main()
