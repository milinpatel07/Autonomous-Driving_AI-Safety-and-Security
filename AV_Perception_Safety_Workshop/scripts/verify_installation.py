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
Installation Verification Script for AV Perception Workshop

Author: Milin Patel
Institution: Hochschule Kempten

Run this script to verify all dependencies are correctly installed.

Usage:
    python scripts/verify_installation.py
"""

import sys
import os


def print_header():
    """Print welcome header"""
    print("=" * 70)
    print(" " * 10 + "AV PERCEPTION & SAFETY WORKSHOP")
    print(" " * 15 + "Installation Verification")
    print("=" * 70)
    print()


def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 8:
        print("   ✅ Python version OK (3.8+)")
        return True
    else:
        print(f"   ❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False


def check_package(package_name, import_name=None, version_attr='__version__'):
    """Check if package is installed and get version"""
    if import_name is None:
        import_name = package_name

    try:
        module = __import__(import_name)
        if hasattr(module, version_attr):
            version = getattr(module, version_attr)
        else:
            version = "installed (version unknown)"
        return True, version
    except ImportError:
        return False, None


def check_core_packages():
    """Check core scientific packages"""
    print("\n📦 Checking core packages...")

    packages = {
        'NumPy': ('numpy', 'numpy'),
        'Pandas': ('pandas', 'pandas'),
        'Matplotlib': ('matplotlib', 'matplotlib'),
        'OpenCV': ('opencv-python', 'cv2'),
    }

    all_ok = True
    for name, (pkg, import_name) in packages.items():
        ok, version = check_package(pkg, import_name)
        if ok:
            print(f"   ✅ {name}: {version}")
        else:
            print(f"   ❌ {name}: Not installed")
            all_ok = False

    return all_ok


def check_deep_learning():
    """Check deep learning frameworks"""
    print("\n🤖 Checking deep learning frameworks...")

    # PyTorch
    ok, version = check_package('torch', 'torch')
    if ok:
        import torch
        print(f"   ✅ PyTorch: {version}")

        # Check CUDA
        if torch.cuda.is_available():
            print(f"      🎮 CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"      CUDA version: {torch.version.cuda}")
        else:
            print(f"      💻 Running on CPU (GPU not available)")
    else:
        print(f"   ❌ PyTorch: Not installed")
        return False

    # Ultralytics (YOLOv8)
    ok, version = check_package('ultralytics', 'ultralytics')
    if ok:
        print(f"   ✅ Ultralytics (YOLOv8): {version}")
    else:
        print(f"   ❌ Ultralytics: Not installed")
        return False

    return True


def check_3d_packages():
    """Check 3D visualization packages"""
    print("\n🎨 Checking 3D visualization...")

    # Open3D
    ok, version = check_package('open3d', 'open3d')
    if ok:
        print(f"   ✅ Open3D: {version}")
    else:
        print(f"   ⚠️  Open3D: Not installed (optional, for LiDAR viz)")
        return False

    return True


def check_dataset_packages():
    """Check dataset handling packages"""
    print("\n📊 Checking dataset packages...")

    packages = [
        ('nuscenes-devkit', 'nuscenes'),
        ('pycocotools', 'pycocotools'),
    ]

    any_installed = False
    for pkg, import_name in packages:
        ok, version = check_package(pkg, import_name)
        if ok:
            print(f"   ✅ {pkg}: {version}")
            any_installed = True
        else:
            print(f"   ⚠️  {pkg}: Not installed (optional)")

    return any_installed


def check_jupyter():
    """Check Jupyter installation"""
    print("\n📓 Checking Jupyter...")

    packages = [
        ('jupyter', 'jupyter'),
        ('jupyterlab', 'jupyterlab'),
        ('ipykernel', 'ipykernel'),
    ]

    all_ok = True
    for pkg, import_name in packages:
        ok, version = check_package(pkg, import_name)
        if ok:
            print(f"   ✅ {pkg}: {version}")
        else:
            print(f"   ❌ {pkg}: Not installed")
            all_ok = False

    return all_ok


def check_directories():
    """Check if workshop directories exist"""
    print("\n📁 Checking workshop structure...")

    required_dirs = [
        'Session_1_AI_Perception_Systems',
        'Session_1_AI_Perception_Systems/notebooks',
        'Session_1_AI_Perception_Systems/scripts',
        'Session_1_AI_Perception_Systems/resources',
        'Session_1_AI_Perception_Systems/exercises',
    ]

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    all_ok = True
    for dir_path in required_dirs:
        full_path = os.path.join(base_path, dir_path)
        if os.path.exists(full_path):
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path}: Not found")
            all_ok = False

    return all_ok


def test_yolo_import():
    """Test if YOLO model can be loaded"""
    print("\n🎯 Testing YOLOv8 model loading...")

    try:
        from ultralytics import YOLO
        print("   Loading YOLOv8n model...")
        model = YOLO('yolov8n.pt')
        print("   ✅ YOLOv8 model loaded successfully")
        return True
    except Exception as e:
        print(f"   ❌ Error loading YOLO: {e}")
        return False


def print_summary(results):
    """Print final summary"""
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    all_passed = all(results.values())

    if all_passed:
        print("\n🎉 ALL CHECKS PASSED!")
        print("\nYou're ready for the workshop!")
        print("\nNext steps:")
        print("  1. Launch Jupyter Lab: jupyter lab")
        print("  2. Navigate to: Session_1_AI_Perception_Systems/notebooks/")
        print("  3. Open: 01_Introduction_SAE_Levels.ipynb")
        print("\n✨ Have fun learning about autonomous vehicle perception! ✨")
    else:
        print("\n⚠️  SOME CHECKS FAILED\n")
        print("Failed components:")
        for check, passed in results.items():
            if not passed:
                print(f"   ❌ {check}")

        print("\nTo fix:")
        print("  1. Ensure virtual environment is activated")
        print("  2. Run: pip install -r requirements.txt")
        print("  3. Re-run this script")
        print("\nFor help, see: setup_instructions.md")

    print("\n" + "=" * 70)


def main():
    """Main verification function"""
    print_header()

    results = {}

    # Run all checks
    results['Python Version'] = check_python_version()
    results['Core Packages'] = check_core_packages()
    results['Deep Learning'] = check_deep_learning()
    results['3D Visualization'] = check_3d_packages()
    results['Dataset Tools'] = check_dataset_packages()
    results['Jupyter'] = check_jupyter()
    results['Directory Structure'] = check_directories()
    results['YOLOv8 Model'] = test_yolo_import()

    # Print summary
    print_summary(results)

    return all(results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
