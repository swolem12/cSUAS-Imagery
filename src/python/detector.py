#!/usr/bin/env python3
"""
Drone Detection System for Raspberry Pi 5
Integrates YOLO models and OpenCV for real-time drone detection
"""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
import argparse


class DroneDetector:
    """Main drone detection class using YOLO and OpenCV"""
    
    def __init__(self, model_path: str, confidence_threshold: float = 0.5,
                 nms_threshold: float = 0.4):
        """
        Initialize the drone detector
        
        Args:
            model_path: Path to the YOLO model weights
            confidence_threshold: Minimum confidence for detections
            nms_threshold: Non-maximum suppression threshold
        """
        self.model_path = Path(model_path)
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.net = None
        self.output_layers = None
        self.classes = ['drone']
        
        self._load_model()
    
    def _load_model(self):
        """Load the YOLO model"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        # Check if using ONNX, PyTorch, or Darknet weights
        model_ext = self.model_path.suffix
        
        if model_ext == '.onnx':
            self.net = cv2.dnn.readNetFromONNX(str(self.model_path))
        elif model_ext == '.weights':
            cfg_path = self.model_path.with_suffix('.cfg')
            if cfg_path.exists():
                self.net = cv2.dnn.readNetFromDarknet(str(cfg_path), str(self.model_path))
        else:
            print(f"Warning: Model format {model_ext} may require additional handling")
            print("For YOLOv8 .pt files, use the ultralytics library")
        
        if self.net is not None:
            # Set backend and target for Raspberry Pi optimization
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            
            # Get output layer names
            layer_names = self.net.getLayerNames()
            self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
    
    def detect(self, image: np.ndarray) -> List[Tuple[int, int, int, int, float]]:
        """
        Detect drones in an image
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            List of detections (x, y, w, h, confidence)
        """
        if self.net is None:
            return []
        
        height, width = image.shape[:2]
        
        # Create blob from image
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        
        # Forward pass
        outputs = self.net.forward(self.output_layers)
        
        # Process detections
        boxes = []
        confidences = []
        
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                confidence = scores[0] if len(scores) > 0 else detection[4]
                
                if confidence > self.confidence_threshold:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
        
        # Apply non-maximum suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)
        
        detections = []
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                detections.append((x, y, w, h, confidences[i]))
        
        return detections
    
    def draw_detections(self, image: np.ndarray, detections: List[Tuple[int, int, int, int, float]]) -> np.ndarray:
        """
        Draw bounding boxes on image
        
        Args:
            image: Input image
            detections: List of detections from detect()
            
        Returns:
            Image with drawn detections
        """
        output_image = image.copy()
        
        for (x, y, w, h, confidence) in detections:
            # Draw bounding box
            cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Draw label
            label = f"Drone: {confidence:.2f}"
            cv2.putText(output_image, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return output_image


def main():
    """Main function for testing the detector"""
    parser = argparse.ArgumentParser(description='Drone Detection System')
    parser.add_argument('--model', type=str, required=True, help='Path to model file')
    parser.add_argument('--source', type=str, default='0', help='Video source (0 for webcam, or path to video)')
    parser.add_argument('--confidence', type=float, default=0.5, help='Confidence threshold')
    parser.add_argument('--nms', type=float, default=0.4, help='NMS threshold')
    parser.add_argument('--output', type=str, help='Output video path (optional)')
    
    args = parser.parse_args()
    
    # Initialize detector
    print(f"Loading model from {args.model}...")
    detector = DroneDetector(args.model, args.confidence, args.nms)
    
    # Open video source
    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source {args.source}")
        return
    
    # Setup video writer if output specified
    writer = None
    if args.output:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(args.output, fourcc, fps, (width, height))
    
    print("Starting detection... Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect drones
        detections = detector.detect(frame)
        
        # Draw detections
        output_frame = detector.draw_detections(frame, detections)
        
        # Display detection count
        count_text = f"Drones detected: {len(detections)}"
        cv2.putText(output_frame, count_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Show frame
        cv2.imshow('Drone Detection', output_frame)
        
        # Write to output if specified
        if writer:
            writer.write(output_frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()
    print("Detection stopped")


if __name__ == '__main__':
    main()
