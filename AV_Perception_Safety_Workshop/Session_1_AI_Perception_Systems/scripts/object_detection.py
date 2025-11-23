# Copyright (c) 2025 Milin Patel
# Hochschule Kempten - University of Applied Sciences
#
# Autonomous Driving: AI Safety and Security Workshop
# Comprehensive educational materials covering AI-based perception, ISO 26262,
# ISO 21448 (SOTIF), ISO/SAE 21434, and uncertainty quantification for autonomous vehicles.
#
# This project is licensed under the MIT License.
# See the LICENSE file in the root directory for full license text.

"""
Object Detection Utilities for AV Perception Workshop

Author: Milin Patel
Institution: Hochschule Kempten

This module provides utility functions for running object detection
on driving scenes using various models (YOLOv8, Faster R-CNN, etc.)
"""

import torch
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Tuple, Optional
import time


class ObjectDetector:
    """
    Wrapper class for object detection models

    Supports:
    - YOLOv8 (nano, small, medium, large, xlarge)
    - Easy inference on images and videos
    - Performance benchmarking
    """

    def __init__(self, model_name: str = 'yolov8n.pt', device: str = 'auto'):
        """
        Initialize object detector

        Args:
            model_name: Model checkpoint name (e.g., 'yolov8n.pt', 'yolov8s.pt')
            device: 'cuda', 'cpu', or 'auto' (auto-select)
        """
        # Set device
        if device == 'auto':
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device

        # Load model
        print(f"Loading {model_name} on {self.device}...")
        self.model = YOLO(model_name)
        self.model.to(self.device)
        print("✅ Model loaded successfully!")

        self.model_name = model_name

    def predict(
        self,
        image: np.ndarray,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45,
        classes: Optional[List[int]] = None
    ) -> Dict:
        """
        Run object detection on a single image

        Args:
            image: Input image (RGB, numpy array)
            conf_threshold: Minimum confidence score (0.0 - 1.0)
            iou_threshold: IoU threshold for NMS
            classes: List of class IDs to detect (None = all classes)

        Returns:
            Dictionary with:
                - boxes: Nx4 array of [x1, y1, x2, y2]
                - confidences: N array of confidence scores
                - class_ids: N array of class IDs
                - class_names: N list of class names
                - inference_time: Inference time in ms
        """
        start_time = time.time()

        # Run inference
        results = self.model.predict(
            image,
            conf=conf_threshold,
            iou=iou_threshold,
            classes=classes,
            verbose=False
        )[0]

        # Synchronize if GPU
        if self.device == 'cuda':
            torch.cuda.synchronize()

        inference_time = (time.time() - start_time) * 1000  # ms

        # Extract results
        boxes = results.boxes.xyxy.cpu().numpy()  # [x1, y1, x2, y2]
        confidences = results.boxes.conf.cpu().numpy()
        class_ids = results.boxes.cls.cpu().numpy().astype(int)
        class_names = [self.model.names[cid] for cid in class_ids]

        return {
            'boxes': boxes,
            'confidences': confidences,
            'class_ids': class_ids,
            'class_names': class_names,
            'inference_time': inference_time
        }

    def visualize(
        self,
        image: np.ndarray,
        detections: Dict,
        show_conf: bool = True,
        thickness: int = 2
    ) -> np.ndarray:
        """
        Draw bounding boxes on image

        Args:
            image: Input image (RGB)
            detections: Detection results from predict()
            show_conf: Show confidence scores
            thickness: Box line thickness

        Returns:
            Image with bounding boxes drawn
        """
        img_vis = image.copy()

        boxes = detections['boxes']
        confidences = detections['confidences']
        class_names = detections['class_names']

        for box, conf, label in zip(boxes, confidences, class_names):
            x1, y1, x2, y2 = box.astype(int)

            # Color based on class
            color = self._get_color(label)

            # Draw box
            cv2.rectangle(img_vis, (x1, y1), (x2, y2), color, thickness)

            # Draw label
            if show_conf:
                text = f"{label}: {conf:.2f}"
            else:
                text = label

            # Text background
            (text_width, text_height), _ = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            cv2.rectangle(
                img_vis,
                (x1, y1 - text_height - 10),
                (x1 + text_width, y1),
                color,
                -1
            )

            # Text
            cv2.putText(
                img_vis, text, (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
            )

        return img_vis

    def _get_color(self, class_name: str) -> Tuple[int, int, int]:
        """
        Get color for class (for visualization)

        Args:
            class_name: Object class name

        Returns:
            RGB color tuple
        """
        # Color scheme for autonomous driving objects
        colors = {
            'person': (255, 0, 0),      # Red (most critical!)
            'car': (0, 255, 0),          # Green
            'truck': (0, 255, 0),
            'bus': (0, 255, 0),
            'bicycle': (255, 165, 0),    # Orange
            'motorcycle': (255, 165, 0),
            'traffic light': (255, 255, 0),  # Yellow
            'stop sign': (255, 0, 255),      # Magenta
        }

        return colors.get(class_name, (0, 0, 255))  # Default: Blue

    def benchmark(
        self,
        image_size: Tuple[int, int] = (640, 640),
        num_runs: int = 50,
        warmup_runs: int = 10
    ) -> Dict:
        """
        Benchmark inference speed

        Args:
            image_size: Test image size (height, width)
            num_runs: Number of benchmark runs
            warmup_runs: Number of warmup runs

        Returns:
            Dictionary with benchmark statistics
        """
        print(f"\n⏱️ Benchmarking {self.model_name} on {self.device}...")

        # Create dummy image
        dummy_img = np.random.randint(
            0, 255, (*image_size, 3), dtype=np.uint8
        )

        # Warm-up
        for _ in range(warmup_runs):
            _ = self.predict(dummy_img)

        # Benchmark
        times = []
        for _ in range(num_runs):
            start = time.time()
            _ = self.predict(dummy_img)
            if self.device == 'cuda':
                torch.cuda.synchronize()
            times.append((time.time() - start) * 1000)  # ms

        # Statistics
        stats = {
            'mean_time': np.mean(times),
            'std_time': np.std(times),
            'min_time': np.min(times),
            'max_time': np.max(times),
            'fps': 1000 / np.mean(times),
            'device': self.device,
            'model': self.model_name
        }

        print(f"\n📊 Benchmark Results ({num_runs} runs):")
        print(f"   - Mean: {stats['mean_time']:.2f} ± {stats['std_time']:.2f} ms")
        print(f"   - FPS: {stats['fps']:.1f}")
        print(f"   - Min: {stats['min_time']:.2f} ms")
        print(f"   - Max: {stats['max_time']:.2f} ms")

        if stats['fps'] >= 30:
            print(f"   ✅ Real-time capable!")
        else:
            print(f"   ⚠️ Below real-time threshold (<30 FPS)")

        return stats


def compute_iou(box1: np.ndarray, box2: np.ndarray) -> float:
    """
    Compute IoU (Intersection over Union) between two boxes

    Args:
        box1: [x1, y1, x2, y2]
        box2: [x1, y1, x2, y2]

    Returns:
        IoU score (0.0 - 1.0)
    """
    # Intersection area
    x1_inter = max(box1[0], box2[0])
    y1_inter = max(box1[1], box2[1])
    x2_inter = min(box1[2], box2[2])
    y2_inter = min(box1[3], box2[3])

    if x2_inter < x1_inter or y2_inter < y1_inter:
        return 0.0

    inter_area = (x2_inter - x1_inter) * (y2_inter - y1_inter)

    # Union area
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = box1_area + box2_area - inter_area

    return inter_area / union_area if union_area > 0 else 0.0


def compute_metrics(
    predictions: List[Dict],
    ground_truth: List[Dict],
    iou_threshold: float = 0.5
) -> Dict:
    """
    Compute detection metrics (precision, recall, F1)

    Args:
        predictions: List of predicted boxes with 'boxes' and 'class_ids'
        ground_truth: List of ground truth boxes
        iou_threshold: IoU threshold for matching

    Returns:
        Dictionary with precision, recall, F1, AP
    """
    # TODO: Implement full metric computation
    # This is a placeholder for workshop participants to implement

    print("⚠️ Full metric computation not yet implemented")
    print("   This is an exercise for participants!")

    return {
        'precision': 0.0,
        'recall': 0.0,
        'f1': 0.0,
        'ap': 0.0
    }


if __name__ == "__main__":
    # Example usage
    print("=" * 60)
    print("Object Detection Module - Test Run")
    print("=" * 60)

    # Initialize detector
    detector = ObjectDetector(model_name='yolov8n.pt')

    # Run benchmark
    stats = detector.benchmark(num_runs=20)

    print("\n✅ Module test complete!")
    print("   Import this module in notebooks to use detection functions.")
