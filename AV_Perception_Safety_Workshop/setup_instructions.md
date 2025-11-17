# Setup Instructions - AV Perception & Safety Workshop

Complete installation guide for all workshop materials.

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Python Environment Setup](#python-environment-setup)
3. [Install Dependencies](#install-dependencies)
4. [Download Datasets](#download-datasets)
5. [Verify Installation](#verify-installation)
6. [Troubleshooting](#troubleshooting)
7. [Optional Components](#optional-components)

---

## 1. System Requirements

### Minimum Requirements
- **OS:** Windows 10/11, macOS 11+, Ubuntu 20.04+
- **Python:** 3.8, 3.9, 3.10, or 3.11
- **RAM:** 8 GB (16 GB recommended)
- **Storage:** 10 GB free space (for datasets)
- **GPU:** Not required (CPU works, but slower)

### Recommended Requirements
- **RAM:** 16 GB or more
- **GPU:** NVIDIA GPU with 6+ GB VRAM (for training)
- **CUDA:** 11.7 or 11.8 (if using GPU)
- **Storage:** 20+ GB for full datasets

### Check Your System
```bash
# Check Python version
python --version  # Should show 3.8.x or higher

# Check if pip is installed
pip --version

# Check CUDA (if NVIDIA GPU)
nvidia-smi  # Should show GPU details
```

---

## 2. Python Environment Setup

### Option A: Conda (Recommended)

```bash
# Create new environment
conda create -n av_workshop python=3.10

# Activate environment
conda activate av_workshop

# Verify
which python  # Should point to av_workshop environment
```

### Option B: venv (Alternative)

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify
which python  # Should point to venv
```

---

## 3. Install Dependencies

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd AV_Perception_Safety_Workshop
```

### Step 2: Upgrade pip

```bash
pip install --upgrade pip setuptools wheel
```

### Step 3: Install PyTorch

**For CPU-only (works everywhere):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**For CUDA 11.8 (NVIDIA GPU):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**For CUDA 12.1 (newer GPUs):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

**Verify PyTorch installation:**
```python
python -c "import torch; print(f'PyTorch {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Step 4: Install Workshop Dependencies

```bash
pip install -r requirements.txt
```

This will take 5-10 minutes depending on your connection.

### Step 5: Install Jupyter

```bash
# Install Jupyter Lab
pip install jupyterlab

# Register kernel
python -m ipykernel install --user --name=av_workshop --display-name="AV Workshop"
```

---

## 4. Download Datasets

### Option A: Automatic Download (Recommended)

```bash
# Download sample datasets for workshop
python scripts/download_datasets.py --samples-only
```

This downloads:
- KITTI sample data (~500 MB)
- nuScenes mini split (~4 GB)
- Sample images from COCO (~200 MB)

**Total:** ~5 GB

### Option B: Manual Download

#### KITTI Dataset
```bash
# Create data directory
mkdir -p data/kitti

# Download raw data (sample)
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/raw_data/2011_09_26_drive_0001/2011_09_26_drive_0001_sync.zip

# Unzip
unzip 2011_09_26_drive_0001_sync.zip -d data/kitti/
```

#### nuScenes Mini
```bash
# Install devkit
pip install nuscenes-devkit

# Download mini split
python -c "from nuscenes import NuScenes; nusc = NuScenes(version='v1.0-mini', dataroot='data/nuscenes', verbose=True)"
```

#### COCO Sample Images
```bash
# Download validation images (1 GB)
mkdir -p data/coco
wget http://images.cocodataset.org/zips/val2017.zip
unzip val2017.zip -d data/coco/

# Download annotations
wget http://images.cocodataset.org/annotations/annotations_trainval2017.zip
unzip annotations_trainval2017.zip -d data/coco/
```

### Option C: No Download (Use Online Datasets)

Skip downloads and use:
- nuScenes web explorer: https://www.nuscenes.org/nuscenes#explore
- Waymo viewer: https://waymo.com/open/viewer/
- Works without local data, requires internet during workshop

---

## 5. Verify Installation

### Run Verification Script

```bash
python scripts/verify_installation.py
```

Expected output:
```
✅ Python version: 3.10.x
✅ PyTorch version: 2.x.x
✅ CUDA available: True (or False if CPU-only)
✅ OpenCV version: 4.x.x
✅ Open3D version: 0.17.x
✅ Jupyter Lab installed
✅ Dataset directory exists
✅ KITTI data found (or warning if not downloaded)
✅ YOLOv8 imports successfully
✅ All dependencies installed!

🎉 Ready for workshop!
```

### Test Jupyter

```bash
# Launch Jupyter Lab
jupyter lab

# In browser: Create new notebook
# Select kernel: "AV Workshop"
# Run:
import torch
import cv2
import open3d as o3d
from ultralytics import YOLO

print("All imports successful!")
```

---

## 6. Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'torch'`

**Solution:**
```bash
# Make sure virtual environment is activated
conda activate av_workshop  # or: source venv/bin/activate

# Reinstall PyTorch
pip install torch torchvision
```

### Issue: PyTorch cannot find CUDA

**Solution:**
```bash
# Check CUDA version
nvidia-smi  # Look at "CUDA Version: X.Y"

# Install matching PyTorch version
# Example for CUDA 11.8:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Issue: `ERROR: Could not build wheels for detectron2`

**Solution:**
Detectron2 is optional. Skip it:
```bash
# Comment out detectron2 line in requirements.txt
# Workshop works fine without it
```

Or install from source:
```bash
pip install 'git+https://github.com/facebookresearch/detectron2.git'
```

### Issue: Open3D visualization not working

**Solution (Linux):**
```bash
# Install OpenGL dependencies
sudo apt-get install libgl1-mesa-glx libglib2.0-0
```

**Solution (macOS):**
```bash
# Install XQuartz for visualization
brew install --cask xquartz
```

**Solution (Windows):**
- Usually works out-of-box
- Update graphics drivers if issues persist

### Issue: nuScenes download fails

**Solution:**
```bash
# Use mini version (smaller)
pip install nuscenes-devkit

# Download manually from:
# https://www.nuscenes.org/nuscenes#download
# Extract to: data/nuscenes/
```

### Issue: Jupyter kernel not found

**Solution:**
```bash
# Reinstall kernel
python -m ipykernel install --user --name=av_workshop --display-name="AV Workshop" --force

# Restart Jupyter
jupyter lab
```

### Issue: Out of memory during training

**Solution:**
```python
# In notebooks, reduce batch size
batch_size = 8  # Change to: 4 or 2

# Or use CPU instead of GPU
device = 'cpu'
```

---

## 7. Optional Components

### Raspberry Pi Setup (Session 4 Live Demo)

If deploying on Raspberry Pi:

```bash
# On Raspberry Pi OS
sudo apt-get update
sudo apt-get install python3-opencv python3-pip

# Install picamera2
pip install picamera2

# Install lightweight PyTorch
pip install https://torch-1.13.0-cp39-cp39-linux_aarch64.whl  # Check version
```

### ROS 2 Integration (Optional)

For advanced users wanting ROS integration:

```bash
# Install ROS 2 Humble (Ubuntu 22.04)
# Follow: https://docs.ros.org/en/humble/Installation.html

# Install ROS Python packages
pip install rclpy sensor_msgs_py
```

### Advanced 3D Visualization (Optional)

```bash
# Install Mayavi (requires VTK)
conda install -c conda-forge mayavi  # Conda recommended

# Or pip:
pip install mayavi
```

---

## ✅ Installation Complete!

You're all set! Next steps:

1. **Launch Jupyter Lab:**
   ```bash
   jupyter lab
   ```

2. **Navigate to Session 1:**
   ```
   Session_1_AI_Perception_Systems/notebooks/
   ```

3. **Open first notebook:**
   ```
   01_Introduction_SAE_Levels.ipynb
   ```

4. **Run all cells** to verify everything works!

---

## 🆘 Still Having Issues?

1. Check our **FAQ:** `docs/FAQ.md`
2. Search **existing issues:** `<repo-url>/issues`
3. Create **new issue** with:
   - OS and Python version
   - Full error message
   - Steps you've tried

---

## 📚 Additional Resources

- **PyTorch Installation:** https://pytorch.org/get-started/locally/
- **Jupyter Documentation:** https://jupyter.org/install
- **CUDA Toolkit:** https://developer.nvidia.com/cuda-downloads
- **nuScenes Setup:** https://github.com/nutonomy/nuscenes-devkit

---

**Ready to start? Let's build autonomous vehicle perception systems! 🚗🤖**

*Last updated: 2025-01-17*
