# OpenPCDet Car Only

This fork of **OpenPCDet** provides configuration and utilities to train single-class
(car) 3D object detectors on datasets arranged in KITTI format.  The repository
also adds Monte‑Carlo dropout support and a simple ensemble script.

## Installation

The project is tested with the following versions:

| Package       | Version |
|---------------|---------|
| Python        | 3.10.13 |
| PyTorch       | 2.2.1   |
| CUDA          | 12.1    |
| cuDNN         | 8902    |
| torchvision   | 0.17.1  |
| spconv        | 2.3.6   |

1. Install PyTorch with CUDA 12.1 (replace the index URL if using a different CUDA version):
   ```bash
   pip install torch==2.2.1+cu121 torchvision==0.17.1+cu121 \
       --extra-index-url https://download.pytorch.org/whl/cu121
   ```
2. Install the remaining dependencies:
   ```bash
   pip install -r requirements.txt
   pip install spconv-cuda12.1 ensemble-boxes
   ```
3. Build the project:
   ```bash
   python setup.py develop
   ```

## Dataset

Place your KITTI formatted dataset under `data/kitti` with the following
structure:

```
data
└── kitti
    ├── ImageSets
    ├── training
    │   ├── image_2
    │   ├── velodyne
    │   ├── label_2
    │   └── calib
    └── testing
        ├── image_2
        ├── velodyne
        └── calib
```

Only the `Car` class should appear in the label files.

## Training

Use the provided configuration for PV-RCNN:

```bash
python tools/train.py --cfg_file tools/cfgs/kitti_models/pv_rcnn_car.yaml
```

## Ensemble and Monte‑Carlo Dropout

* Monte‑Carlo dropout is enabled when `MC_DROPOUT: True` in model configs.
* To ensemble multiple checkpoints:

```bash
python tools/ensemble.py --cfg_file tools/cfgs/kitti_models/pv_rcnn_car.yaml \
    --ckpts ckpt1.pth ckpt2.pth
```

Fused results are saved to `ensemble_output/ensemble_result.pkl`.

## Docker

A simple Dockerfile is provided to create an environment matching the
above versions.  Build with

```bash
docker build -t openpcdet_car .
```

and run with

```bash
docker run --gpus all -it openpcdet_car
```
