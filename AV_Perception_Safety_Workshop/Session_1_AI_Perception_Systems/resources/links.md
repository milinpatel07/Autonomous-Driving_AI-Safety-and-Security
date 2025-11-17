# Session 1: Useful Links and Online Resources

**Last Updated:** 2025-01-17

This document contains curated links to online tools, demos, and resources used in Session 1.

---

## 📊 Interactive Demos & Tools

### Object Detection Demos

1. **YOLOv8/v9 Web Demo** (Hugging Face)
   - Link: https://huggingface.co/spaces/Xenova/yolov9-web
   - Description: Upload images and see real-time object detection
   - Use: Demo 1 in Session 1
   - Works: In browser, no installation needed

2. **Roboflow Universe - Object Detection Models**
   - Link: https://universe.roboflow.com/explore
   - Description: Browse and test 50,000+ trained models
   - Features: Upload images, use webcam, custom models
   - Great for: Exploring different detection models

3. **YOLOv8 Gradio Demo** (Alternative)
   - Link: https://huggingface.co/spaces/merve/YOLO-NAS-detection
   - Description: Faster alternative to Xenova demo
   - Use: Backup if main demo is slow

### Dataset Explorers

4. **nuScenes Dataset Explorer** ⭐ HIGHLY RECOMMENDED
   - Link: https://www.nuscenes.org/nuscenes#explore
   - Description: Browse real autonomous driving data
   - Features:
     - Toggle camera, LiDAR, radar views
     - See annotations
     - Multiple scenes (Boston, Singapore)
   - Use: Demo 2 in Session 1

5. **Waymo Open Dataset Viewer**
   - Link: https://waymo.com/open/viewer/
   - Description: 3D visualization of Waymo's dataset
   - Features:
     - Interactive 3D point clouds
     - Camera and LiDAR fusion
     - 1000+ driving scenes
   - Use: Dataset exploration

6. **KITTI Vision Benchmark Suite**
   - Link: http://www.cvlibs.net/datasets/kitti/raw_data.php
   - Description: Classic autonomous driving benchmark
   - Features: Download individual sequences
   - Use: Historical reference, still widely used

7. **Scale AI Open Dataset Browser**
   - Link: https://scale.com/open-av-datasets
   - Description: Compare multiple AV datasets
   - Features:
     - Side-by-side sensor comparison
     - Multiple datasets in one place
   - Use: Quick sensor modality comparison

8. **Segments.ai Autonomous Driving Explorer**
   - Link: https://segments.ai/explore
   - Filter by: "Autonomous Driving"
   - Description: Annotated datasets from multiple sources
   - Features: Toggle annotation layers

### Sensor Visualizations

9. **Open3D Web Visualizer**
   - Link: http://www.open3d.org/docs/latest/tutorial/visualization/web_visualizer.html
   - Description: Visualize 3D point clouds in browser
   - Use: LiDAR data exploration

10. **CNN Explainer** (Optional - Deep Dive)
    - Link: https://poloclub.github.io/cnn-explainer/
    - Description: Interactive visualization of how CNNs work
    - Use: Understanding "black box" neural networks

---

## 🎥 Video Resources

### Sensor Technology

11. **Waymo: How Our Sensors Work** (Official)
    - Link: https://www.youtube.com/watch?v=B8R148hFxPw
    - Duration: 3 minutes
    - Content: Camera, LiDAR, radar visualization
    - Use: Show in slides (Slide 7-11)

12. **Camera vs LiDAR vs Radar Comparison**
    - Link: https://www.youtube.com/watch?v=eviOUScPCCg
    - Duration: ~3 minutes
    - Content: Direct side-by-side comparison
    - Use: Sensor modalities explanation

13. **LiDAR Point Cloud Visualization**
    - Link: https://www.youtube.com/watch?v=KXpZ6B1YB_k
    - Duration: 2 minutes
    - Content: 3D point cloud rotation and visualization
    - Use: Understanding LiDAR output

14. **How Radar Works in Autonomous Vehicles**
    - Link: https://www.youtube.com/watch?v=GXI2ZcrewWk
    - Duration: ~5 minutes
    - Content: Radar perception demo
    - Use: Radar sensor explanation

### Object Detection & AI

15. **How Tesla Autopilot Works** (Andrej Karpathy Talk)
    - Link: https://www.youtube.com/watch?v=uxLBcPdKfbs
    - Duration: 5 minutes (excerpt from longer talk)
    - Content: Neural network processing for vision
    - Use: AI in perception explanation

16. **YOLO Object Detection Explained**
    - Link: https://www.youtube.com/watch?v=ag3DLKsl2vk
    - Duration: ~10 minutes
    - Content: How YOLO algorithm works
    - Use: Deep dive (optional)

### Safety & Testing

17. **Euro NCAP Pedestrian AEB Tests**
    - Link: https://www.youtube.com/watch?v=3_38KHlS1zQ
    - Duration: 4 minutes
    - Content: Real pedestrian detection + braking tests
    - Use: Case study (Slide 14), bridge to Session 2

18. **Mercedes Drive Pilot (Level 3 Demo)**
    - Link: https://www.youtube.com/watch?v=fmJvLfL_NfA
    - Duration: ~5 minutes
    - Content: First Level 3 production system
    - Use: SAE levels example

---

## 📚 Official Documentation & Standards

### Standards

19. **SAE J3016 - Levels of Driving Automation**
    - Link: https://www.sae.org/standards/content/j3016_202104/
    - Description: Official SAE standard (requires purchase for full text)
    - Free Summary: https://www.sae.org/news/2019/01/sae-updates-j3016-automated-driving-graphic

20. **ISO 26262 - Functional Safety**
    - Link: https://www.iso.org/standard/68383.html
    - Description: Functional safety for road vehicles
    - Use: Reference for Session 3

21. **ISO 21448 (SOTIF) - Safety of Intended Functionality**
    - Link: https://www.iso.org/standard/77490.html
    - Description: Handling scenarios not covered by ISO 26262
    - Use: Session 3 (critical for AI systems!)

22. **ISO 8800 - Safety & Artificial Intelligence**
    - Link: https://www.iso.org/standard/83303.html
    - Status: Recently published (2024)
    - Description: AI-specific safety requirements
    - Use: Session 3-4

### Open Source Projects

23. **Apollo Auto (Baidu)**
    - Link: https://github.com/ApolloAuto/apollo
    - Description: Open-source autonomous driving platform
    - Use: Reference architecture, code examples

24. **Autoware Foundation**
    - Link: https://github.com/autowarefoundation/autoware
    - Description: Open-source AV software (ROS-based)
    - Use: Perception module examples

25. **OpenPCDet** ⭐ (You're already here!)
    - Link: https://github.com/open-mmlab/OpenPCDet
    - Description: 3D object detection from point clouds
    - Use: LiDAR perception

### Deep Learning Frameworks

26. **Ultralytics YOLOv8 Documentation**
    - Link: https://docs.ultralytics.com/
    - Description: Official YOLOv8 docs, tutorials, examples
    - Use: Primary detection framework for workshop

27. **Detectron2 (Facebook AI)**
    - Link: https://github.com/facebookresearch/detectron2
    - Description: Alternative object detection framework
    - Use: Optional, advanced users

---

## 🗺️ Dataset Download Instructions

### KITTI Dataset

28. **KITTI Vision Benchmark**
    - Homepage: http://www.cvlibs.net/datasets/kitti/
    - Download:
      - Raw data: http://www.cvlibs.net/datasets/kitti/raw_data.php
      - Object detection: http://www.cvlibs.net/datasets/kitti/eval_object.php
    - Size: ~165 GB (full), samples available
    - Register: Required for download

### nuScenes Dataset

29. **nuScenes by Motional**
    - Homepage: https://www.nuscenes.org/nuscenes
    - Download: https://www.nuscenes.org/nuscenes#download
    - Versions:
      - Full: 1.4M images, ~350 GB
      - Mini: 1/10 size, ~4 GB (recommended for workshop)
      - Trainval: Training and validation split
    - Register: Required

### Waymo Open Dataset

30. **Waymo Open Dataset**
    - Homepage: https://waymo.com/open/
    - Download: https://waymo.com/open/download/
    - Size: ~1 TB (perception dataset)
    - Format: TFRecord (TensorFlow)
    - Register: Google account required

### BDD100K

31. **Berkeley DeepDrive 100K**
    - Homepage: https://bdd-data.berkeley.edu/
    - Download: https://bdd-data.berkeley.edu/portal.html#download
    - Size: 100K video sequences, ~1.8 TB
    - Features: Diverse weather, geography, time
    - Register: Required

### COCO Dataset (General Purpose)

32. **COCO - Common Objects in Context**
    - Homepage: https://cocodataset.org/
    - Download: https://cocodataset.org/#download
    - Versions:
      - Train: 118K images (~18 GB)
      - Val: 5K images (~1 GB) ← Recommended for testing
    - Use: YOLOv8 pre-trained on this

---

## 🔬 Research Papers (Key References)

33. **YOLOv8 Paper**
    - ArXiv: https://arxiv.org/abs/2305.09972
    - Year: 2023
    - Topic: Latest YOLO architecture

34. **nuScenes Dataset Paper**
    - ArXiv: https://arxiv.org/abs/1903.11027
    - Year: 2019
    - Topic: First full-sensor suite AV dataset

35. **PointPillars (LiDAR Detection)**
    - ArXiv: https://arxiv.org/abs/1812.05784
    - Year: 2018
    - Topic: Fast 3D object detection

36. **Multi-Task Learning for Dense Prediction (Tesla)**
    - ArXiv: https://arxiv.org/abs/1809.04766
    - Year: 2018 (Karpathy et al.)
    - Topic: How Tesla processes camera data

---

## 🛠️ Tools & Software

37. **Download Tools**
    - **wget**: Command-line downloader (Linux/Mac)
    - **4K Video Downloader**: YouTube videos for offline use
      - Link: https://www.4kdownload.com/
    - **ytdl**: YouTube download via Python
      - `pip install yt-dlp`

38. **Visualization Tools**
    - **CVAT** (Computer Vision Annotation Tool)
      - Link: https://www.cvat.ai/
      - Use: Annotate your own data
    - **Labelbox**
      - Link: https://labelbox.com/
      - Use: Professional annotation platform

---

## 📖 Learning Resources

39. **Autonomous Driving Course (Coursera - University of Toronto)**
    - Link: https://www.coursera.org/specializations/self-driving-cars
    - Content: Full AV specialization
    - Level: Intermediate to advanced

40. **Deep Learning for Self-Driving Cars (MIT)**
    - Link: https://selfdrivingcars.mit.edu/
    - Content: Lectures, tutorials, code
    - Level: Advanced

41. **Comma.ai Open Pilot**
    - Link: https://comma.ai/
    - GitHub: https://github.com/commaai/openpilot
    - Description: Open-source driving assist system
    - Use: Real-world implementation example

---

## ⚠️ Backup & Offline Resources

If **internet is unavailable** during workshop:

1. **Pre-download:**
   - YOLOv8 model weights (`yolov8n.pt`)
   - 10-20 sample images from COCO/KITTI
   - nuScenes mini dataset
   - Key YouTube videos (use 4K Video Downloader)

2. **Offline demos:**
   - Run object detection locally (Notebook 3)
   - Use downloaded images
   - Load local nuScenes data

3. **Screen recordings:**
   - Record nuScenes explorer session
   - Record Waymo viewer session
   - Play back as videos

---

## 🆘 Troubleshooting

**Link doesn't work?**
- Check if URL changed (search for service name)
- Try Wayback Machine: https://web.archive.org/
- Use alternative demos listed above

**Demo is slow?**
- Try backup demos
- Use local inference (Notebook 3)
- Download dataset for offline use

**Dataset download fails?**
- Use mini/sample versions
- Download via torrents (if available)
- Use online explorers instead

---

## 📧 Feedback

Found a broken link or have a suggestion?
- Open an issue on GitHub
- Email: [your-email]

---

*Last updated: 2025-01-17*
*Maintained by: Milin Patel, Hochschule Kempten*
