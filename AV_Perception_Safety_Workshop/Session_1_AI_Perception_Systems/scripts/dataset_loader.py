"""
Dataset Loading Utilities for AV Perception Workshop

Author: Milin Patel
Institution: Hochschule Kempten

This module provides loaders for:
- KITTI Dataset
- nuScenes Dataset (if available)
- Waymo Open Dataset (if available)
- Sample/synthetic data generation
"""

import numpy as np
import os
from typing import Optional, Tuple, Dict, List
import cv2
from pathlib import Path
import warnings


class KITTILoader:
    """
    Loader for KITTI dataset format

    Expected structure:
    kitti/
    ├── training/
    │   ├── image_2/
    │   ├── velodyne/
    │   ├── label_2/
    │   └── calib/
    └── testing/
        ├── image_2/
        ├── velodyne/
        └── calib/
    """

    def __init__(self, data_root: str, split: str = 'training'):
        """
        Initialize KITTI loader

        Args:
            data_root: Path to KITTI dataset root
            split: 'training' or 'testing'
        """
        self.data_root = Path(data_root)
        self.split = split
        self.split_dir = self.data_root / split

        # Check if dataset exists
        if not self.split_dir.exists():
            warnings.warn(f"KITTI {split} directory not found: {self.split_dir}")
            self.available = False
        else:
            self.available = True

        self.image_dir = self.split_dir / 'image_2'
        self.velodyne_dir = self.split_dir / 'velodyne'
        self.label_dir = self.split_dir / 'label_2'
        self.calib_dir = self.split_dir / 'calib'

        # Get number of samples
        if self.available and self.image_dir.exists():
            self.num_samples = len(list(self.image_dir.glob('*.png')))
        else:
            self.num_samples = 0

    def get_image(self, idx: int) -> Optional[np.ndarray]:
        """Load camera image"""
        if not self.available:
            return None

        img_path = self.image_dir / f'{idx:06d}.png'
        if not img_path.exists():
            return None

        img = cv2.imread(str(img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img

    def get_velodyne(self, idx: int) -> Optional[np.ndarray]:
        """Load LiDAR point cloud"""
        if not self.available:
            return None

        velo_path = self.velodyne_dir / f'{idx:06d}.bin'
        if not velo_path.exists():
            return None

        # KITTI velodyne format: Nx4 (x, y, z, intensity)
        points = np.fromfile(str(velo_path), dtype=np.float32)
        points = points.reshape(-1, 4)
        return points

    def get_calibration(self, idx: int) -> Optional[Dict[str, np.ndarray]]:
        """Load calibration matrices"""
        if not self.available:
            return None

        calib_path = self.calib_dir / f'{idx:06d}.txt'
        if not calib_path.exists():
            return None

        calib = {}
        with open(calib_path, 'r') as f:
            for line in f:
                if line.strip():
                    key, *values = line.split()
                    key = key.rstrip(':')
                    values = np.array([float(v) for v in values])

                    if key == 'P2':
                        calib['P'] = values.reshape(3, 4)
                    elif key == 'R0_rect':
                        R0 = values.reshape(3, 3)
                        calib['R0_rect'] = np.eye(4)
                        calib['R0_rect'][:3, :3] = R0
                    elif key == 'Tr_velo_to_cam':
                        Tr = values.reshape(3, 4)
                        calib['Tr_velo_to_cam'] = np.eye(4)
                        calib['Tr_velo_to_cam'][:3, :] = Tr

        return calib

    def get_labels(self, idx: int) -> Optional[List[Dict]]:
        """Load object labels"""
        if not self.available or self.split == 'testing':
            return None

        label_path = self.label_dir / f'{idx:06d}.txt'
        if not label_path.exists():
            return None

        objects = []
        with open(label_path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.split()
                    obj = {
                        'type': parts[0],
                        'truncated': float(parts[1]),
                        'occluded': int(parts[2]),
                        'alpha': float(parts[3]),
                        'bbox': np.array([float(x) for x in parts[4:8]]),  # 2D bbox
                        'dimensions': np.array([float(x) for x in parts[8:11]]),  # h, w, l
                        'location': np.array([float(x) for x in parts[11:14]]),  # x, y, z
                        'rotation_y': float(parts[14])
                    }
                    objects.append(obj)

        return objects

    def get_frame(self, idx: int) -> Dict:
        """
        Load complete frame with all data

        Returns:
            Dictionary with 'image', 'pointcloud', 'calibration', 'labels'
        """
        frame = {
            'idx': idx,
            'image': self.get_image(idx),
            'pointcloud': self.get_velodyne(idx),
            'calibration': self.get_calibration(idx),
            'labels': self.get_labels(idx),
            'available': self.available
        }
        return frame

    def __len__(self) -> int:
        return self.num_samples

    def __getitem__(self, idx: int) -> Dict:
        return self.get_frame(idx)


class NuScenesLoader:
    """
    Loader for nuScenes dataset (requires nuscenes-devkit)
    """

    def __init__(self, data_root: str, version: str = 'v1.0-mini'):
        """
        Initialize nuScenes loader

        Args:
            data_root: Path to nuScenes dataset root
            version: Dataset version ('v1.0-mini', 'v1.0-trainval', etc.)
        """
        self.data_root = data_root
        self.version = version

        try:
            from nuscenes.nuscenes import NuScenes
            self.nusc = NuScenes(version=version, dataroot=data_root, verbose=False)
            self.available = True
            print(f"✅ nuScenes {version} loaded: {len(self.nusc.scene)} scenes")
        except ImportError:
            warnings.warn("nuscenes-devkit not installed. Install with: pip install nuscenes-devkit")
            self.available = False
            self.nusc = None
        except Exception as e:
            warnings.warn(f"Could not load nuScenes dataset: {e}")
            self.available = False
            self.nusc = None

    def get_sample(self, sample_token: str) -> Optional[Dict]:
        """Get sample data by token"""
        if not self.available:
            return None

        sample = self.nusc.get('sample', sample_token)
        return sample

    def get_sample_data(self, sample_data_token: str) -> Tuple[str, np.ndarray, np.ndarray]:
        """Get sample data (image or pointcloud) with path and ego pose"""
        if not self.available:
            return None, None, None

        from nuscenes.nuscenes import NuScenes
        from nuscenes.utils.data_classes import LidarPointCloud

        # Get data path
        data_path, boxes, camera_intrinsic = self.nusc.get_sample_data(sample_data_token)

        return data_path, boxes, camera_intrinsic

    def __len__(self) -> int:
        if self.available:
            return len(self.nusc.sample)
        return 0


class WaymoLoader:
    """
    Loader for Waymo Open Dataset (requires waymo-open-dataset)
    """

    def __init__(self, data_root: str):
        """
        Initialize Waymo loader

        Args:
            data_root: Path to Waymo dataset root (tfrecord files)
        """
        self.data_root = data_root

        try:
            from waymo_open_dataset import dataset_pb2
            self.available = True
            print("✅ Waymo Open Dataset loader initialized")
        except ImportError:
            warnings.warn("waymo-open-dataset not installed. Install with: pip install waymo-open-dataset-tf-2-11-0")
            self.available = False


class SyntheticDataGenerator:
    """
    Generate synthetic sample data for testing and demonstrations
    """

    @staticmethod
    def generate_sample_image(
        scene_type: str = 'urban',
        size: Tuple[int, int] = (1242, 375)
    ) -> np.ndarray:
        """
        Generate synthetic driving scene image

        Args:
            scene_type: 'urban', 'highway', or 'residential'
            size: Image size (width, height)

        Returns:
            RGB image
        """
        w, h = size
        img = np.zeros((h, w, 3), dtype=np.uint8)

        if scene_type == 'urban':
            # Sky
            img[:h//3, :] = [135, 206, 235]  # Light blue
            # Buildings
            for i in range(5):
                x = np.random.randint(0, w-100)
                building_h = np.random.randint(h//4, h*2//3)
                color = np.random.randint(100, 180, 3)
                cv2.rectangle(img, (x, h-building_h), (x+100, h), color.tolist(), -1)
            # Road
            img[h*2//3:, :] = [70, 70, 70]
            # Lane markings
            for x in range(0, w, 50):
                cv2.rectangle(img, (x, h-10), (x+20, h-5), (255, 255, 255), -1)

        elif scene_type == 'highway':
            # Sky
            img[:h//2, :] = [135, 206, 250]
            # Ground
            img[h//2:, :] = [100, 120, 100]
            # Road
            road_top = h*2//3
            img[road_top:, :] = [60, 60, 60]
            # Lane markings
            for y in range(road_top, h, 30):
                cv2.line(img, (w//2, y), (w//2, y+15), (255, 255, 255), 3)

        else:  # residential
            # Sky
            img[:h//2, :] = [135, 206, 235]
            # Trees
            img[h//2:h*2//3, :] = [34, 139, 34]
            # Road
            img[h*2//3:, :] = [50, 50, 50]

        return img

    @staticmethod
    def generate_sample_pointcloud(
        scene_type: str = 'urban',
        num_points: int = 10000
    ) -> np.ndarray:
        """
        Generate synthetic point cloud

        Args:
            scene_type: 'urban', 'highway', or 'residential'
            num_points: Number of points to generate

        Returns:
            Nx4 array (x, y, z, intensity)
        """
        if scene_type == 'urban':
            # Ground plane
            ground = np.random.uniform([-30, 0, -1.8], [30, 50, -1.5], (num_points//2, 3))
            ground_intensity = np.random.uniform(0.1, 0.3, (num_points//2, 1))

            # Buildings and objects
            objects = np.random.uniform([-30, 5, -1.5], [30, 50, 5], (num_points//2, 3))
            objects_intensity = np.random.uniform(0.3, 0.9, (num_points//2, 1))

            points = np.hstack([
                np.vstack([ground, objects]),
                np.vstack([ground_intensity, objects_intensity])
            ])

        elif scene_type == 'highway':
            # Mostly road surface
            road = np.random.uniform([-20, 0, -1.8], [20, 100, -1.5], (num_points*3//4, 3))
            road_intensity = np.random.uniform(0.1, 0.3, (num_points*3//4, 1))

            # Some barriers and vehicles
            objects = np.random.uniform([-20, 10, -1.5], [20, 80, 2], (num_points//4, 3))
            objects_intensity = np.random.uniform(0.4, 0.8, (num_points//4, 1))

            points = np.hstack([
                np.vstack([road, objects]),
                np.vstack([road_intensity, objects_intensity])
            ])

        else:  # residential
            # Ground
            ground = np.random.uniform([-20, 0, -1.8], [20, 40, -1.5], (num_points//3, 3))
            ground_intensity = np.random.uniform(0.2, 0.4, (num_points//3, 1))

            # Vegetation
            trees = np.random.uniform([-20, 5, -1], [20, 35, 5], (num_points//3, 3))
            trees_intensity = np.random.uniform(0.1, 0.5, (num_points//3, 1))

            # Houses
            houses = np.random.uniform([-20, 10, -1], [20, 35, 4], (num_points//3, 3))
            houses_intensity = np.random.uniform(0.4, 0.7, (num_points//3, 1))

            points = np.hstack([
                np.vstack([ground, trees, houses]),
                np.vstack([ground_intensity, trees_intensity, houses_intensity])
            ])

        return points

    @staticmethod
    def generate_sample_labels(scene_type: str = 'urban') -> List[Dict]:
        """
        Generate sample object labels

        Args:
            scene_type: Scene type

        Returns:
            List of object dictionaries
        """
        labels = []

        if scene_type == 'urban':
            # Add cars
            for i in range(np.random.randint(3, 8)):
                labels.append({
                    'type': 'Car',
                    'bbox': np.random.randint([200, 200, 300, 250]),
                    'location': np.random.uniform([-10, 10, 0], [10, 30, 0]),
                    'dimensions': np.array([1.5, 4.0, 1.6]),  # h, l, w
                    'confidence': np.random.uniform(0.8, 0.99)
                })

            # Add pedestrians
            for i in range(np.random.randint(1, 4)):
                labels.append({
                    'type': 'Pedestrian',
                    'bbox': np.random.randint([300, 250, 350, 350]),
                    'location': np.random.uniform([-5, 15, 0], [5, 25, 0]),
                    'dimensions': np.array([1.7, 0.6, 0.6]),
                    'confidence': np.random.uniform(0.7, 0.95)
                })

        elif scene_type == 'highway':
            # Mostly cars
            for i in range(np.random.randint(5, 12)):
                labels.append({
                    'type': 'Car',
                    'bbox': np.random.randint([100, 200, 200, 280]),
                    'location': np.random.uniform([-15, 20, 0], [15, 60, 0]),
                    'dimensions': np.array([1.5, 4.2, 1.7]),
                    'confidence': np.random.uniform(0.85, 0.99)
                })

        return labels


def download_sample_data(output_dir: str = 'data/samples') -> None:
    """
    Download or generate sample data for testing

    Args:
        output_dir: Where to save sample data
    """
    os.makedirs(output_dir, exist_ok=True)

    print("📦 Generating sample data...")

    gen = SyntheticDataGenerator()

    # Generate sample images
    for scene_type in ['urban', 'highway', 'residential']:
        img = gen.generate_sample_image(scene_type)
        img_path = os.path.join(output_dir, f'sample_{scene_type}.png')
        cv2.imwrite(img_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(f"✅ Generated: {img_path}")

    # Generate sample point clouds
    for scene_type in ['urban', 'highway']:
        points = gen.generate_sample_pointcloud(scene_type, num_points=15000)
        pc_path = os.path.join(output_dir, f'sample_{scene_type}.bin')
        points.astype(np.float32).tofile(pc_path)
        print(f"✅ Generated: {pc_path}")

    print(f"\n✅ Sample data saved to: {output_dir}")


if __name__ == "__main__":
    print("=" * 70)
    print("Dataset Loader Module - Test")
    print("=" * 70)
    print()

    # Test synthetic data generation
    print("🧪 Testing synthetic data generation...")
    gen = SyntheticDataGenerator()

    img = gen.generate_sample_image('urban')
    print(f"✅ Generated sample image: {img.shape}")

    points = gen.generate_sample_pointcloud('urban', num_points=5000)
    print(f"✅ Generated sample pointcloud: {points.shape}")

    labels = gen.generate_sample_labels('urban')
    print(f"✅ Generated {len(labels)} sample labels")
    print()

    # Test KITTI loader (if available)
    print("🔍 Testing KITTI loader...")
    kitti = KITTILoader('data/kitti', split='training')
    if kitti.available:
        print(f"✅ KITTI dataset found: {len(kitti)} samples")
    else:
        print("⚠️ KITTI dataset not found (this is OK for testing)")
    print()

    print("✅ Module test complete!")
