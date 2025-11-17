"""
General Utility Functions for AV Perception Workshop

Author: Milin Patel
Institution: Hochschule Kempten

This module provides helper functions for:
- Image loading and processing
- Dataset downloading
- Visualization
- Metrics computation
"""

import cv2
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from typing import Optional, Tuple, List
import os
import urllib.request
from tqdm import tqdm


def load_image(path_or_url: str, rgb: bool = True) -> np.ndarray:
    """
    Load image from file path or URL

    Args:
        path_or_url: Local file path or HTTP(S) URL
        rgb: Convert to RGB (default: True)

    Returns:
        Image as numpy array
    """
    if path_or_url.startswith('http'):
        # Load from URL
        response = requests.get(path_or_url)
        img = Image.open(BytesIO(response.content))
        img = np.array(img)
    else:
        # Load from file
        img = cv2.imread(path_or_url)
        if rgb:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img


def download_file(url: str, output_path: str, show_progress: bool = True) -> None:
    """
    Download file from URL with progress bar

    Args:
        url: Download URL
        output_path: Where to save file
        show_progress: Show tqdm progress bar
    """
    if os.path.exists(output_path):
        print(f"✅ File already exists: {output_path}")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if show_progress:
        # Download with progress bar
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(output_path, 'wb') as f, tqdm(
            desc=os.path.basename(output_path),
            total=total_size,
            unit='B',
            unit_scale=True
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))
    else:
        # Simple download
        urllib.request.urlretrieve(url, output_path)

    print(f"✅ Downloaded: {output_path}")


def resize_image(
    image: np.ndarray,
    target_size: Optional[Tuple[int, int]] = None,
    max_size: Optional[int] = None,
    keep_aspect: bool = True
) -> np.ndarray:
    """
    Resize image

    Args:
        image: Input image
        target_size: Target (width, height), overrides max_size
        max_size: Maximum dimension (maintains aspect ratio)
        keep_aspect: Keep aspect ratio

    Returns:
        Resized image
    """
    h, w = image.shape[:2]

    if target_size is not None:
        new_w, new_h = target_size
    elif max_size is not None:
        if max(h, w) > max_size:
            if h > w:
                new_h = max_size
                new_w = int(w * (max_size / h)) if keep_aspect else max_size
            else:
                new_w = max_size
                new_h = int(h * (max_size / w)) if keep_aspect else max_size
        else:
            return image
    else:
        return image

    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)


def draw_boxes(
    image: np.ndarray,
    boxes: np.ndarray,
    labels: Optional[List[str]] = None,
    colors: Optional[List[Tuple[int, int, int]]] = None,
    thickness: int = 2
) -> np.ndarray:
    """
    Draw bounding boxes on image

    Args:
        image: Input image (RGB)
        boxes: Nx4 array of [x1, y1, x2, y2]
        labels: List of N labels (optional)
        colors: List of N colors (optional)
        thickness: Line thickness

    Returns:
        Image with boxes drawn
    """
    img_vis = image.copy()

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box.astype(int)

        # Color
        if colors is not None:
            color = colors[i]
        else:
            color = (0, 255, 0)  # Default: Green

        # Draw box
        cv2.rectangle(img_vis, (x1, y1), (x2, y2), color, thickness)

        # Draw label
        if labels is not None and i < len(labels):
            text = labels[i]
            cv2.putText(
                img_vis, text, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
            )

    return img_vis


def create_color_map(num_colors: int) -> List[Tuple[int, int, int]]:
    """
    Create distinct colors for visualization

    Args:
        num_colors: Number of colors needed

    Returns:
        List of RGB color tuples
    """
    colors = []
    for i in range(num_colors):
        hue = int(180 * i / num_colors)
        # HSV to RGB
        hsv = np.uint8([[[hue, 255, 255]]])
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)[0][0]
        colors.append(tuple(int(c) for c in rgb))

    return colors


def compute_precision_recall(
    tp: int, fp: int, fn: int
) -> Tuple[float, float, float]:
    """
    Compute precision, recall, and F1 score

    Args:
        tp: True positives
        fp: False positives
        fn: False negatives

    Returns:
        (precision, recall, f1)
    """
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return precision, recall, f1


def verify_installation() -> bool:
    """
    Verify all required packages are installed

    Returns:
        True if all packages available
    """
    print("🔍 Verifying installation...\n")

    packages = {
        'PyTorch': None,
        'OpenCV': None,
        'NumPy': None,
        'Matplotlib': None,
        'Ultralytics (YOLOv8)': None,
        'Open3D': None,
    }

    # Check PyTorch
    try:
        import torch
        packages['PyTorch'] = torch.__version__
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            packages['PyTorch'] += f" (CUDA {torch.version.cuda})"
        else:
            packages['PyTorch'] += " (CPU only)"
    except ImportError:
        packages['PyTorch'] = "❌ Not installed"

    # Check OpenCV
    try:
        import cv2
        packages['OpenCV'] = cv2.__version__
    except ImportError:
        packages['OpenCV'] = "❌ Not installed"

    # Check NumPy
    try:
        import numpy
        packages['NumPy'] = numpy.__version__
    except ImportError:
        packages['NumPy'] = "❌ Not installed"

    # Check Matplotlib
    try:
        import matplotlib
        packages['Matplotlib'] = matplotlib.__version__
    except ImportError:
        packages['Matplotlib'] = "❌ Not installed"

    # Check Ultralytics
    try:
        import ultralytics
        packages['Ultralytics (YOLOv8)'] = ultralytics.__version__
    except ImportError:
        packages['Ultralytics (YOLOv8)'] = "❌ Not installed"

    # Check Open3D
    try:
        import open3d
        packages['Open3D'] = open3d.__version__
    except ImportError:
        packages['Open3D'] = "❌ Not installed"

    # Print results
    all_ok = True
    for pkg, version in packages.items():
        if "❌" in str(version):
            print(f"❌ {pkg}: {version}")
            all_ok = False
        else:
            print(f"✅ {pkg}: {version}")

    print()
    if all_ok:
        print("🎉 All packages installed correctly!")
    else:
        print("⚠️ Some packages missing. Run: pip install -r requirements.txt")

    return all_ok


if __name__ == "__main__":
    print("=" * 60)
    print("Utility Module - Installation Verification")
    print("=" * 60)
    print()

    verify_installation()

    print("\n✅ Module test complete!")
