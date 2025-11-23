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
Workshop Setup Script - Generates sample data and verifies installation

Author: Milin Patel
Institution: Hochschule Kempten
"""

import os
import sys
import numpy as np
import cv2
from pathlib import Path

def create_sample_images():
    """Generate sample driving scene images"""
    print("📸 Generating sample images...")

    output_dir = Path("Session_1_AI_Perception_Systems/data/sample_images")
    output_dir.mkdir(parents=True, exist_ok=True)

    scenes = {
        'urban_scene.jpg': (1242, 375, 'urban'),
        'highway_traffic.jpg': (1242, 375, 'highway'),
        'residential_street.jpg': (1242, 375, 'residential')
    }

    for filename, (w, h, scene_type) in scenes.items():
        img = generate_scene_image(w, h, scene_type)
        output_path = output_dir / filename
        cv2.imwrite(str(output_path), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(f"   ✅ {filename}")

    print(f"✅ Generated {len(scenes)} sample images\n")

def generate_scene_image(width, height, scene_type):
    """Generate synthetic scene image"""
    img = np.zeros((height, width, 3), dtype=np.uint8)

    if scene_type == 'urban':
        # Sky
        img[:height//3, :] = [135, 206, 235]
        # Buildings
        for i in range(6):
            x = i * (width // 6)
            building_h = np.random.randint(height//4, height*2//3)
            color = np.random.randint(80, 150, 3).tolist()
            cv2.rectangle(img, (x, height-building_h), (x+width//6, height), color, -1)
            # Windows
            for wx in range(x+10, x+width//6-10, 30):
                for wy in range(height-building_h+20, height-20, 40):
                    cv2.rectangle(img, (wx, wy), (wx+15, wy+25), [255, 255, 200], -1)
        # Road
        img[height*2//3:, :] = [70, 70, 70]
        # Lane markings
        for x in range(50, width, 100):
            cv2.rectangle(img, (x, height-30), (x+40, height-20), [255, 255, 255], -1)
        # Add some cars
        car_positions = [(200, height-100), (500, height-110), (900, height-105)]
        for x, y in car_positions:
            cv2.rectangle(img, (x, y), (x+80, y+50), [180, 50, 50], -1)
            cv2.rectangle(img, (x+10, y+10), (x+30, y+25), [100, 150, 200], -1)
            cv2.rectangle(img, (x+50, y+10), (x+70, y+25), [100, 150, 200], -1)

    elif scene_type == 'highway':
        # Sky
        img[:height//2, :] = [135, 206, 250]
        # Ground/vegetation
        img[height//2:height*2//3, :] = [100, 140, 80]
        # Road
        img[height*2//3:, :] = [60, 60, 60]
        # Lane markings
        lane_y = height*2//3
        for y in range(int(lane_y), height, 40):
            cv2.rectangle(img, (width//2-5, y), (width//2+5, y+20), [255, 255, 255], -1)
        # Highway barriers
        cv2.rectangle(img, (50, int(lane_y)), (80, height), [200, 200, 200], -1)
        cv2.rectangle(img, (width-80, int(lane_y)), (width-50, height), [200, 200, 200], -1)

    else:  # residential
        # Sky
        img[:height//2, :] = [135, 206, 235]
        # Trees/vegetation
        img[height//2:height*2//3, :] = [34, 139, 34]
        for i in range(8):
            x = np.random.randint(0, width)
            cv2.circle(img, (x, height//2 + 20), 40, [34, 100, 34], -1)
        # Road
        img[height*2//3:, :] = [50, 50, 50]
        # Sidewalk
        cv2.rectangle(img, (0, height*2//3), (100, height), [150, 150, 150], -1)
        cv2.rectangle(img, (width-100, height*2//3), (width, height), [150, 150, 150], -1)

    return img

def create_sample_pointclouds():
    """Generate sample point clouds"""
    print("🌐 Generating sample point clouds...")

    output_dir = Path("Session_1_AI_Perception_Systems/data/sample_pointclouds")
    output_dir.mkdir(parents=True, exist_ok=True)

    scenes = {
        'urban_scene.bin': ('urban', 15000),
        'highway_scene.bin': ('highway', 12000)
    }

    for filename, (scene_type, num_points) in scenes.items():
        points = generate_scene_pointcloud(scene_type, num_points)
        output_path = output_dir / filename
        points.astype(np.float32).tofile(str(output_path))
        print(f"   ✅ {filename} ({num_points} points)")

    print(f"✅ Generated {len(scenes)} sample point clouds\n")

def generate_scene_pointcloud(scene_type, num_points):
    """Generate synthetic point cloud"""
    if scene_type == 'urban':
        # Ground
        ground = np.random.uniform([-30, 0, -1.8], [30, 50, -1.5], (num_points//2, 3))
        ground_intensity = np.random.uniform(0.1, 0.3, (num_points//2, 1))

        # Buildings and objects
        objects = np.random.uniform([-30, 5, -1.5], [30, 50, 5], (num_points//2, 3))
        objects_intensity = np.random.uniform(0.3, 0.9, (num_points//2, 1))

        points = np.hstack([
            np.vstack([ground, objects]),
            np.vstack([ground_intensity, objects_intensity])
        ])

    else:  # highway
        # Road
        road = np.random.uniform([-20, 0, -1.8], [20, 100, -1.5], (num_points*3//4, 3))
        road_intensity = np.random.uniform(0.1, 0.3, (num_points*3//4, 1))

        # Barriers and vehicles
        objects = np.random.uniform([-20, 10, -1.5], [20, 80, 2], (num_points//4, 3))
        objects_intensity = np.random.uniform(0.4, 0.8, (num_points//4, 1))

        points = np.hstack([
            np.vstack([road, objects]),
            np.vstack([road_intensity, objects_intensity])
        ])

    return points

def verify_installation():
    """Verify all required packages"""
    print("🔍 Verifying installation...\n")

    required_packages = {
        'torch': 'PyTorch',
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib',
        'ultralytics': 'YOLOv8',
    }

    all_ok = True
    for module_name, display_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} - NOT INSTALLED")
            all_ok = False

    print()
    if all_ok:
        print("🎉 All required packages installed!\n")
    else:
        print("⚠️ Some packages missing. Run: pip install -r requirements.txt\n")

    return all_ok

def main():
    """Main setup function"""
    print("="*70)
    print("AV Perception & Safety Workshop - Setup")
    print("="*70)
    print()

    # Change to workshop directory
    workshop_dir = Path(__file__).parent
    os.chdir(workshop_dir)

    # Verify installation
    if not verify_installation():
        print("⚠️ Please install missing packages first!")
        return

    # Create sample data
    try:
        create_sample_images()
        create_sample_pointclouds()
        print("✅ Workshop setup complete!")
        print("\n📚 Next steps:")
        print("   1. cd Session_1_AI_Perception_Systems")
        print("   2. jupyter lab")
        print("   3. Open notebooks/01_Introduction_SAE_Levels.ipynb")
        print("\n🚀 Happy learning!")
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
