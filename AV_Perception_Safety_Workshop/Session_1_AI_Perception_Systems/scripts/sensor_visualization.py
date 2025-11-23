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
Sensor Visualization Utilities for AV Perception Workshop

Author: Milin Patel
Institution: Hochschule Kempten

This module provides functions for:
- 3D point cloud visualization
- LiDAR to camera projection
- Multi-sensor data overlay
- Interactive 3D viewers
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import cm
from typing import Optional, Tuple, List, Dict
import warnings

# Try to import Open3D (for 3D visualization)
try:
    import open3d as o3d
    OPEN3D_AVAILABLE = True
except ImportError:
    OPEN3D_AVAILABLE = False
    warnings.warn("Open3D not available. 3D visualization will be limited.")

# Try to import plotly (for interactive plots)
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    warnings.warn("Plotly not available. Interactive plots will use matplotlib.")


def visualize_pointcloud(
    points: np.ndarray,
    colors: Optional[np.ndarray] = None,
    color_by: str = 'distance',
    point_size: float = 2.0,
    title: str = "3D Point Cloud",
    use_plotly: bool = False
) -> None:
    """
    Visualize 3D point cloud

    Args:
        points: Nx3 array of (x, y, z) coordinates
        colors: Nx3 array of RGB colors (0-1 range), optional
        color_by: 'distance', 'height', 'intensity', or 'uniform'
        point_size: Size of points in visualization
        title: Plot title
        use_plotly: Use interactive plotly viewer (if available)
    """
    if use_plotly and PLOTLY_AVAILABLE:
        _visualize_pointcloud_plotly(points, colors, color_by, title)
    elif OPEN3D_AVAILABLE:
        _visualize_pointcloud_open3d(points, colors, color_by, point_size, title)
    else:
        _visualize_pointcloud_matplotlib(points, colors, color_by, title)


def _visualize_pointcloud_open3d(
    points: np.ndarray,
    colors: Optional[np.ndarray],
    color_by: str,
    point_size: float,
    title: str
) -> None:
    """Visualize using Open3D"""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])

    if colors is not None:
        pcd.colors = o3d.utility.Vector3dVector(colors)
    else:
        # Color by specified attribute
        pcd_colors = _compute_point_colors(points, color_by)
        pcd.colors = o3d.utility.Vector3dVector(pcd_colors)

    # Visualize
    print(f"🎨 Visualizing {len(points)} points...")
    print("💡 Use mouse to rotate, scroll to zoom")
    o3d.visualization.draw_geometries(
        [pcd],
        window_name=title,
        width=1024,
        height=768,
        point_show_normal=False
    )


def _visualize_pointcloud_plotly(
    points: np.ndarray,
    colors: Optional[np.ndarray],
    color_by: str,
    title: str
) -> None:
    """Visualize using Plotly (interactive)"""
    if colors is None:
        colors = _compute_point_colors(points, color_by)

    # Convert RGB to hex colors
    hex_colors = ['#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
                  for r, g, b in colors]

    fig = go.Figure(data=[go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode='markers',
        marker=dict(
            size=2,
            color=hex_colors,
            opacity=0.8
        )
    )])

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (m)',
            yaxis_title='Y (m)',
            zaxis_title='Z (m)',
            aspectmode='data'
        ),
        width=1000,
        height=800
    )

    fig.show()


def _visualize_pointcloud_matplotlib(
    points: np.ndarray,
    colors: Optional[np.ndarray],
    color_by: str,
    title: str
) -> None:
    """Visualize using Matplotlib (static)"""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    if colors is None:
        colors = _compute_point_colors(points, color_by)

    # Subsample for performance
    max_points = 10000
    if len(points) > max_points:
        idx = np.random.choice(len(points), max_points, replace=False)
        points = points[idx]
        colors = colors[idx]

    ax.scatter(
        points[:, 0], points[:, 1], points[:, 2],
        c=colors, s=1, alpha=0.6
    )

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title(title)

    # Equal aspect ratio
    max_range = np.array([
        points[:, 0].max()-points[:, 0].min(),
        points[:, 1].max()-points[:, 1].min(),
        points[:, 2].max()-points[:, 2].min()
    ]).max() / 2.0

    mid_x = (points[:, 0].max()+points[:, 0].min()) * 0.5
    mid_y = (points[:, 1].max()+points[:, 1].min()) * 0.5
    mid_z = (points[:, 2].max()+points[:, 2].min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.tight_layout()
    plt.show()


def _compute_point_colors(points: np.ndarray, color_by: str) -> np.ndarray:
    """Compute colors for points based on attribute"""
    if color_by == 'distance':
        # Color by distance from origin
        distances = np.linalg.norm(points[:, :3], axis=1)
        normalized = (distances - distances.min()) / (distances.max() - distances.min() + 1e-6)
    elif color_by == 'height':
        # Color by Z coordinate
        normalized = (points[:, 2] - points[:, 2].min()) / (points[:, 2].max() - points[:, 2].min() + 1e-6)
    elif color_by == 'intensity' and points.shape[1] >= 4:
        # Color by intensity (4th column)
        normalized = points[:, 3]
        normalized = (normalized - normalized.min()) / (normalized.max() - normalized.min() + 1e-6)
    else:
        # Uniform color
        return np.tile([0.5, 0.5, 0.5], (len(points), 1))

    # Map to colormap
    colormap = cm.get_cmap('viridis')
    colors = colormap(normalized)[:, :3]  # RGB only

    return colors


def project_lidar_to_camera(
    points: np.ndarray,
    image: np.ndarray,
    calibration: Dict[str, np.ndarray],
    min_distance: float = 0.0,
    max_distance: float = 70.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Project 3D LiDAR points onto 2D camera image

    Args:
        points: Nx3 or Nx4 array of (x, y, z, [intensity])
        image: Camera image (RGB)
        calibration: Dict with 'P' (projection matrix) and 'R0_rect', 'Tr_velo_to_cam'
        min_distance: Minimum point distance to include
        max_distance: Maximum point distance to include

    Returns:
        image_coords: Nx2 array of (u, v) image coordinates
        depths: N array of distances
        valid_mask: N boolean array of valid projections
    """
    # Get calibration matrices
    P = calibration.get('P', np.eye(3, 4))  # Projection matrix
    R0_rect = calibration.get('R0_rect', np.eye(4))  # Rectification
    Tr_velo_to_cam = calibration.get('Tr_velo_to_cam', np.eye(4))  # Transform

    # Transform points to camera coordinate system
    pts_3d_homo = np.hstack([points[:, :3], np.ones((len(points), 1))])
    pts_cam = pts_3d_homo @ Tr_velo_to_cam.T @ R0_rect.T

    # Filter points in front of camera
    valid_depth = (pts_cam[:, 2] > min_distance) & (pts_cam[:, 2] < max_distance)

    # Project to image
    pts_2d_homo = pts_cam @ P.T
    pts_2d = pts_2d_homo[:, :2] / (pts_2d_homo[:, 2:3] + 1e-6)

    # Filter points within image bounds
    h, w = image.shape[:2]
    valid_x = (pts_2d[:, 0] >= 0) & (pts_2d[:, 0] < w)
    valid_y = (pts_2d[:, 1] >= 0) & (pts_2d[:, 1] < h)

    valid_mask = valid_depth & valid_x & valid_y

    return pts_2d, pts_cam[:, 2], valid_mask


def overlay_lidar_on_image(
    image: np.ndarray,
    points: np.ndarray,
    calibration: Dict[str, np.ndarray],
    color_by: str = 'distance',
    point_size: int = 3
) -> np.ndarray:
    """
    Overlay LiDAR points on camera image

    Args:
        image: Camera image (RGB)
        points: Nx3 or Nx4 LiDAR points
        calibration: Calibration matrices
        color_by: 'distance' or 'height'
        point_size: Size of overlay points

    Returns:
        Image with LiDAR overlay
    """
    img_overlay = image.copy()

    # Project points
    pts_2d, depths, valid = project_lidar_to_camera(points, image, calibration)

    # Color by attribute
    if color_by == 'distance':
        values = depths[valid]
    elif color_by == 'height':
        values = points[valid, 2]
    else:
        values = depths[valid]

    # Normalize and map to colormap
    normalized = (values - values.min()) / (values.max() - values.min() + 1e-6)
    colormap = cm.get_cmap('jet')
    colors = colormap(normalized)[:, :3] * 255  # RGB 0-255

    # Draw points
    for (u, v), color in zip(pts_2d[valid].astype(int), colors):
        cv2.circle(img_overlay, (u, v), point_size, color.tolist(), -1)

    return img_overlay


def compare_sensor_views(
    camera_image: np.ndarray,
    lidar_points: np.ndarray,
    calibration: Optional[Dict[str, np.ndarray]] = None,
    radar_data: Optional[np.ndarray] = None
) -> None:
    """
    Compare different sensor modalities side-by-side

    Args:
        camera_image: RGB camera image
        lidar_points: Nx3 point cloud
        calibration: Calibration for LiDAR-camera projection
        radar_data: Radar detections (optional)
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Camera view
    axes[0].imshow(camera_image)
    axes[0].set_title('📷 Camera (RGB)', fontsize=14, fontweight='bold')
    axes[0].axis('off')

    # LiDAR overlay
    if calibration is not None:
        lidar_overlay = overlay_lidar_on_image(
            camera_image, lidar_points, calibration,
            color_by='distance', point_size=2
        )
        axes[1].imshow(lidar_overlay)
        axes[1].set_title('🌐 LiDAR Overlay', fontsize=14, fontweight='bold')
    else:
        axes[1].imshow(camera_image)
        axes[1].text(0.5, 0.5, 'No Calibration Data',
                    ha='center', va='center', transform=axes[1].transAxes)
        axes[1].set_title('🌐 LiDAR (No Calib)', fontsize=14, fontweight='bold')
    axes[1].axis('off')

    # Bird's eye view (LiDAR)
    bev = create_birds_eye_view(lidar_points, image_size=(400, 400))
    axes[2].imshow(bev, cmap='viridis')
    axes[2].set_title("🗺️ Bird's Eye View", fontsize=14, fontweight='bold')
    axes[2].axis('off')

    plt.tight_layout()
    plt.show()


def create_birds_eye_view(
    points: np.ndarray,
    image_size: Tuple[int, int] = (512, 512),
    x_range: Tuple[float, float] = (-40, 40),
    y_range: Tuple[float, float] = (0, 80),
    z_range: Tuple[float, float] = (-3, 3)
) -> np.ndarray:
    """
    Create bird's eye view (top-down) from point cloud

    Args:
        points: Nx3 point cloud
        image_size: Output image size (height, width)
        x_range: (min, max) range in meters (lateral)
        y_range: (min, max) range in meters (forward)
        z_range: (min, max) height range to include

    Returns:
        Bird's eye view image
    """
    h, w = image_size

    # Filter points by Z
    mask = (points[:, 2] >= z_range[0]) & (points[:, 2] <= z_range[1])
    points_filtered = points[mask]

    # Convert to pixel coordinates
    x_img = (points_filtered[:, 0] - x_range[0]) / (x_range[1] - x_range[0]) * w
    y_img = (points_filtered[:, 1] - y_range[0]) / (y_range[1] - y_range[0]) * h

    # Filter valid pixels
    valid = (x_img >= 0) & (x_img < w) & (y_img >= 0) & (y_img < h)
    x_img = x_img[valid].astype(int)
    y_img = y_img[valid].astype(int)

    # Create image
    bev = np.zeros((h, w), dtype=np.float32)

    # Accumulate points
    for x, y in zip(x_img, y_img):
        bev[h - 1 - y, x] += 1  # Flip Y for image coordinates

    # Normalize
    if bev.max() > 0:
        bev = np.clip(bev / bev.max(), 0, 1)

    return bev


def load_sample_pointcloud(sample_type: str = 'urban') -> np.ndarray:
    """
    Generate synthetic sample point cloud for testing

    Args:
        sample_type: 'urban', 'highway', or 'random'

    Returns:
        Nx3 point cloud
    """
    if sample_type == 'urban':
        # Simulate urban scene with buildings, ground, cars
        ground = np.random.uniform([-30, 0, -1.8], [30, 50, -1.5], (5000, 3))
        buildings_left = np.random.uniform([-30, 5, -1.5], [-15, 40, 5], (3000, 3))
        buildings_right = np.random.uniform([15, 5, -1.5], [30, 40, 5], (3000, 3))
        cars = np.random.uniform([-10, 10, -1.5], [10, 30, 1], (1000, 3))
        points = np.vstack([ground, buildings_left, buildings_right, cars])
    elif sample_type == 'highway':
        # Simulate highway scene
        road = np.random.uniform([-20, 0, -1.8], [20, 100, -1.5], (8000, 3))
        barriers = np.random.uniform([-20, 0, -1.5], [-18, 100, 0.5], (1000, 3))
        points = np.vstack([road, barriers])
    else:
        # Random points
        points = np.random.uniform([-30, 0, -2], [30, 50, 5], (10000, 3))

    return points


def visualize_sensor_comparison_table() -> None:
    """Display sensor comparison table"""
    data = [
        ['Sensor', 'Range', 'Resolution', 'Weather', 'Cost', 'Use Case'],
        ['Camera', '100m', 'High (2MP+)', '❌ Poor (rain/fog)', '💰 Low', 'Classification, signs'],
        ['LiDAR', '200m', 'High (0.1°)', '⚠️ Medium (fog)', '💰💰💰 High', '3D detection, mapping'],
        ['Radar', '250m', 'Low', '✅ Excellent', '💰💰 Medium', 'Speed, all-weather']
    ]

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(
        cellText=data,
        cellLoc='left',
        loc='center',
        colWidths=[0.12, 0.12, 0.18, 0.22, 0.16, 0.20]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)

    # Style header row
    for i in range(6):
        cell = table[(0, i)]
        cell.set_facecolor('#4CAF50')
        cell.set_text_props(weight='bold', color='white')

    # Style data rows
    for i in range(1, 4):
        for j in range(6):
            cell = table[(i, j)]
            cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')

    plt.title('📊 Autonomous Vehicle Sensor Comparison',
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("=" * 70)
    print("Sensor Visualization Module - Test")
    print("=" * 70)
    print()

    print("🔍 Testing sensor visualization functions...")
    print()

    # Generate sample point cloud
    print("📊 Generating sample point cloud...")
    points = load_sample_pointcloud('urban')
    print(f"✅ Generated {len(points)} points")
    print()

    # Test bird's eye view
    print("🗺️ Creating bird's eye view...")
    bev = create_birds_eye_view(points)
    print(f"✅ BEV shape: {bev.shape}")
    print()

    # Show comparison table
    print("📋 Displaying sensor comparison table...")
    visualize_sensor_comparison_table()
    print()

    # Test 3D visualization
    print("🎨 Testing 3D visualization...")
    print("💡 Close the window to continue...")
    visualize_pointcloud(points[::10], color_by='height', title="Sample Urban Scene")

    print("\n✅ Module test complete!")
