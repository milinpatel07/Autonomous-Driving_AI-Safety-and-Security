# Datasets and Benchmarks

**Module 10: Autonomous Driving Datasets, Evaluation Metrics, and Benchmark Analysis**

---

## Overview

High-quality datasets and rigorous benchmarking are fundamental to autonomous vehicle development. This module provides comprehensive coverage of major autonomous driving datasets (KITTI, nuScenes, Waymo Open Dataset), evaluation metrics for perception tasks, statistical dataset analysis, bias assessment, and best practices for custom dataset creation. Students learn to critically evaluate datasets, understand their limitations, and apply appropriate metrics for performance assessment.

### Module Objectives

Upon completing this module, you will:

1. **Master Key Datasets**: Understand KITTI, nuScenes, Waymo Open Dataset, and other major benchmarks
2. **Apply Evaluation Metrics**: Compute and interpret Average Precision (AP), mean AP (mAP), and IoU for detection
3. **Analyze Dataset Statistics**: Perform statistical analysis of object distributions, sensor coverage, and scenario diversity
4. **Assess Dataset Bias**: Identify geographic, temporal, and demographic biases in training data
5. **Understand Limitations**: Recognize dataset gaps and their impact on model generalization
6. **Design Custom Datasets**: Apply best practices for data collection, annotation, and quality assurance
7. **Benchmark Models**: Compare state-of-the-art models using standardized evaluation protocols
8. **Connect to Safety**: Understand dataset quality implications for ISO 26262, SOTIF, and AI safety

---

## Why Datasets and Benchmarks Matter

### Critical Challenges in Autonomous Driving Data

**1. Dataset Scale and Diversity**
- **KITTI (2012)**: 7,481 training images, 80,000 labeled objects
  - Limitation: Small scale, single city (Karlsruhe, Germany)
  - Weather: Primarily clear/overcast, limited adverse conditions
  - Still widely used for benchmarking due to established baseline
- **nuScenes (2019)**: 1,000 scenes (20s each), 1.4M annotated objects
  - Full sensor suite: 6 cameras (360°), 1 LiDAR, 5 radars
  - Boston and Singapore data - more geographic diversity
  - Weather diversity: Rain, night driving
- **Waymo Open Dataset (2020)**: 1,000 segments (200,000 frames), 12M 3D labels
  - Largest public dataset, diverse weather and locations
  - High-quality multi-modal annotations
- **Challenge**: Even largest datasets cover tiny fraction of possible scenarios

**2. Evaluation Metric Limitations**
- **Average Precision (AP)**: Standard metric but has critical limitations
  - Assumes all false positives equally bad (not true for safety)
  - Doesn't account for consequence of errors (missed pedestrian vs. missed parked car)
  - Threshold-dependent: AP@IoU=0.5 vs. AP@IoU=0.7 can differ significantly
- **mAP (mean Average Precision)**: Averages across object classes
  - Treats all classes equally (pedestrian same weight as traffic cone)
  - High mAP doesn't guarantee safety-critical class performance
- **SOTIF consideration**: Need safety-weighted metrics, not just statistical accuracy

**3. Geographic and Temporal Bias**
- **Geographic bias**:
  - Most datasets: US (California, Arizona), Europe (Germany), Asia (Singapore)
  - Missing: South America, Africa, Middle East, rural areas globally
  - Infrastructure differences: Road markings, signage, vehicle types
  - Driving culture variations not captured
- **Temporal bias**:
  - Dataset collection year: 2012 (KITTI), 2019 (nuScenes), 2020 (Waymo)
  - New vehicle types appear over time (e-scooters, delivery robots)
  - Infrastructure changes (new traffic patterns, construction)
  - **Distribution shift**: Models degrade over time without retraining

**4. Weather and Lighting Imbalance**
- **Overrepresentation**: Clear weather, daytime, dry roads
  - Easier for data collection, better annotation quality
  - Models learn these conditions well
- **Underrepresentation**: Heavy rain, fog, snow, night, low sun angle
  - Harder to collect (safety concerns)
  - Annotation more difficult (lower quality labels)
  - **Safety concern**: Models fail precisely when conditions are most dangerous
- **SOTIF triggering conditions**: Underrepresented scenarios are performance limitations

**5. Annotation Quality and Consistency**
- **Inter-annotator agreement**: Different annotators label same scene differently
  - Pedestrian vs. cyclist in low light
  - Occluded object boundaries uncertain
  - Target: >95% IoU agreement for safety-critical objects
- **Annotation errors**:
  - Missing objects (false negatives in ground truth)
  - Incorrect bounding boxes (size, orientation)
  - Class confusion (truck vs. van)
  - **Problem**: Models learn from imperfect labels
- **Quality assurance**: Multi-stage review, automated consistency checks essential

**6. Sensor Configuration Differences**
- **KITTI**: Velodyne HDL-64E LiDAR, stereo cameras
- **nuScenes**: Velodyne HDL-32E LiDAR, 6 cameras, 5 radars
- **Waymo**: Custom LiDAR sensors (75m range top, 360° perimeter), 5 cameras
- **Problem**: Models trained on one dataset don't transfer well to different sensor configs
- **Domain adaptation required**: Fine-tuning on target sensor configuration

**7. Long-Tail Scenario Underrepresentation**
- **Pareto principle**: 80% of driving is common scenarios, 20% is diverse edge cases
- **Datasets skew toward common**: Highways, clear weather, standard vehicles
- **Rare but critical scenarios underrepresented**:
  - Emergency vehicles, construction zones, unusual pedestrian behavior
  - Animals on road, objects falling from trucks
  - Infrastructure failures (missing signs, damaged roads)
- **SOTIF challenge**: Unknown unsafe scenarios exist beyond dataset coverage

---

## Module Structure

### 📓 Notebooks

1. **[01_dataset_overview.ipynb](notebooks/01_dataset_overview.ipynb)**
   - KITTI Vision Benchmark: 2D/3D object detection, tracking, segmentation
   - nuScenes: Full sensor suite, 360° perception, tracking IDs
   - Waymo Open Dataset: Large-scale multi-modal annotations
   - Argoverse 2: HD maps and forecasting
   - Cityscapes: Urban semantic segmentation
   - BDD100K: Diverse driving conditions (100,000 videos)
   - A2D2: Audi dataset with semantic segmentation
   - Dataset comparison matrix: Size, sensors, annotations, diversity

2. **[02_dataset_analysis.ipynb](notebooks/02_dataset_analysis.ipynb)**
   - Object class distribution: Histogram analysis, long-tail visualization
   - Spatial distribution: Object locations in ego vehicle frame
   - Temporal analysis: Object trajectories and behavior patterns
   - Weather and lighting statistics: Percentage clear/rain/night
   - Geographic coverage: Cities and environments represented
   - Sensor coverage analysis: Occlusion patterns, range limitations
   - Bias quantification: Chi-square test for distribution differences

3. **[03_benchmark_metrics.ipynb](notebooks/03_benchmark_metrics.ipynb)**
   - Intersection over Union (IoU): 2D and 3D variants
   - Average Precision (AP): Precision-recall curves, AP calculation
   - mean Average Precision (mAP): Multi-class aggregation
   - Orientation similarity: Bird's Eye View (BEV) metrics
   - Tracking metrics: MOTA (Multi-Object Tracking Accuracy), MOTP, IDF1
   - Semantic segmentation: mIoU (mean Intersection over Union)
   - Safety-weighted metrics: Class-specific thresholds
   - Leaderboard analysis: KITTI, nuScenes, Waymo benchmarks

4. **[04_custom_dataset_creation.ipynb](notebooks/04_custom_dataset_creation.ipynb)**
   - Data collection planning: ODD definition, scenario coverage
   - Sensor selection and calibration: Intrinsic and extrinsic parameters
   - Annotation guidelines: Consistency, edge case handling
   - Quality assurance pipeline: Multi-stage review, automated checks
   - Dataset statistics and balance: Ensuring diversity
   - Train/validation/test split: Avoiding data leakage
   - Dataset documentation: Datasheets for datasets, model cards
   - Ethical considerations: Privacy, consent, demographic representation

---

## Prerequisites

### Knowledge
- Understanding of perception systems (Module 01)
- Familiarity with object detection and segmentation
- Basic statistics and data analysis
- Python programming

### Software
- Python 3.8+
- Dataset devkits: KITTI, nuScenes, Waymo Open Dataset
- Libraries: NumPy, Pandas, Matplotlib, Open3D
- Optional: ROS for sensor data handling

---

## Dataset Tools and Frameworks

- **KITTI DevKit**: MATLAB/Python evaluation scripts
- **nuScenes DevKit**: Python API for data access and evaluation
- **Waymo Open Dataset Tools**: TensorFlow-based data loaders
- **Scalabel**: Open-source annotation platform
- **CVAT**: Computer Vision Annotation Tool
- **Datumaro**: Dataset management framework

---

## Learning Path

### Beginner Path
1. Start with **01_dataset_overview** to understand major datasets
2. Proceed to **03_benchmark_metrics** for evaluation fundamentals
3. Learn **02_dataset_analysis** for statistical understanding

### Advanced Path
4. Master **04_custom_dataset_creation** for data collection and quality assurance

---

## Practical Exercises

Located in `exercises/`:
1. **Exercise 1**: Load and visualize KITTI 3D object detection data
2. **Exercise 2**: Compute mAP for YOLOv5 on nuScenes validation set
3. **Exercise 3**: Analyze weather distribution bias in Waymo Open Dataset
4. **Exercise 4**: Compare pedestrian detection AP across KITTI, nuScenes, Waymo
5. **Exercise 5**: Design data collection plan for urban delivery robot ODD

---

## Code Examples

Located in `code/`:
- `dataset_loader.py`: Unified interface for KITTI, nuScenes, Waymo
- `evaluation_metrics.py`: AP, mAP, IoU implementations
- `dataset_statistics.py`: Distribution analysis and visualization
- `annotation_validator.py`: Quality assurance checks
- `benchmark_comparison.py`: Multi-dataset model evaluation

---

## Industry Standards and References

### Standards
- **ISO/IEC 25012**: Data Quality Model
- **ISO/PAS 8800**: Data quality requirements for AI safety
- **ISO 21448 (SOTIF)**: Scenario coverage and dataset representativeness
- **ISO/IEC 24029-1**: Assessment of robustness of neural networks
- **IEEE P2851**: Functional Safety Data Format for Automated Driving

### Key Papers
- Geiger et al. (2012): "Are we ready for Autonomous Driving? The KITTI Vision Benchmark Suite"
- Caesar et al. (2020): "nuScenes: A multimodal dataset for autonomous driving"
- Sun et al. (2020): "Scalability in Perception for Autonomous Driving: Waymo Open Dataset"
- Gebru et al. (2018): "Datasheets for Datasets" - Dataset documentation framework
- Mitchell et al. (2019): "Model Cards for Model Reporting" - Model documentation
- Torralba & Efros (2011): "Unbiased Look at Dataset Bias"

### Resources
- [KITTI Benchmark](http://www.cvlibs.net/datasets/kitti/)
- [nuScenes Dataset](https://www.nuscenes.org/)
- [Waymo Open Dataset](https://waymo.com/open/)
- [Papers With Code - Autonomous Driving Benchmarks](https://paperswithcode.com/task/autonomous-driving)
- [Roboflow Universe - Datasets](https://universe.roboflow.com/)

---

## Learning Outcomes Assessment

By the end of this module, you should be able to:

✓ Understand structure and characteristics of major AV datasets
✓ Compute and interpret AP, mAP, and IoU metrics
✓ Perform statistical analysis of dataset distributions
✓ Identify geographic, temporal, and demographic biases
✓ Evaluate dataset quality and annotation consistency
✓ Compare model performance across different benchmarks
✓ Design custom datasets with proper coverage and quality
✓ Apply dataset documentation best practices (datasheets)
✓ Understand dataset limitations for SOTIF validation

---

## Integration with Other Modules

### Prerequisites
- **Module 01**: Perception Systems - Understanding what is being evaluated

### Related Modules
- **Module 02**: Failure Analysis - Dataset bias as source of failures
- **Module 04**: SOTIF - Dataset coverage and scenario identification
- **Module 06**: AI Safety - Data quality and distribution shift
- **Module 07**: Validation & Verification - Benchmark-based testing

### Application Modules
- **Module 09**: LiDAR Technology - 3D annotation and point cloud datasets
- **Module 10**: Use datasets from this module throughout all practical exercises

---

## Next Steps

After completing this module:
- Apply datasets to implement perception systems (Module 01)
- Analyze dataset gaps for SOTIF validation (Module 04)
- Use datasets for uncertainty quantification research (Module 06)
- Design custom datasets for specific ODD and safety validation

---

**Author:** Milin Patel
**Institution:** Hochschule Kempten - University of Applied Sciences
**License:** MIT
**Last Updated:** 2025-12-28
