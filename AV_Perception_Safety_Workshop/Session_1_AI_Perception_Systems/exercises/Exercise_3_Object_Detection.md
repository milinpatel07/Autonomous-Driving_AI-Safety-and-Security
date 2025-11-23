# Exercise 3: Object Detection Performance Analysis

**Session 1: AI-based Perception Systems**
**Difficulty:** Intermediate

---

## 🎯 Learning Objectives

After completing this exercise, you will be able to:
- Run object detection on driving scenes
- Analyze confidence scores and their meaning
- Understand precision-recall trade-offs
- Identify detection failure modes
- Tune confidence thresholds for safety requirements

---

## Prerequisites

- Completed Notebook 3: Object Detection Demo
- Python environment with YOLOv8 installed
- Test images (from COCO, KITTI, or your own)

---

## Part A: Basic Detection

### Task 1: Run Detection on Test Images

Use the code from Notebook 3 to detect objects in **5 different driving scenes**:

1. **Urban intersection** (multiple vehicles, pedestrians)
2. **Highway traffic** (vehicles at distance)
3. **Pedestrian crossing** (close-up pedestrians)
4. **Night scene** (low light)
5. **Rain/fog** (adverse weather)

**Record your results:**

| Image | Objects Detected | Avg Confidence | Missed Objects | False Positives |
|-------|------------------|----------------|----------------|-----------------|
| 1. Urban | | | | |
| 2. Highway | | | | |
| 3. Pedestrian | | | | |
| 4. Night | | | | |
| 5. Rain/Fog | | | | |

**Code to use:**
```python
from scripts.object_detection import ObjectDetector

detector = ObjectDetector(model_name='yolov8n.pt')
results = detector.predict(image, conf_threshold=0.25)
```

---

### Task 2: Analyze Confidence Scores

For **Image 1 (Urban)**:

1. **List all detections with confidence > 0.7 (high confidence):**
   ```


   ```

2. **List all detections with confidence 0.3 - 0.7 (medium confidence):**
   ```


   ```

3. **What do you notice about confidence scores?**
   - Are all pedestrians detected with high confidence?
   - Are distant objects detected with lower confidence?
   - Your observations:
   ```


   ```

---

## Part B: Confidence Threshold Tuning

### Task 3: Precision-Recall Trade-off

Run detection on **Image 3 (Pedestrian Crossing)** with **three different thresholds**:

| Threshold | Pedestrians Detected | False Positives | Missed Pedestrians |
|-----------|---------------------|-----------------|-------------------|
| 0.25 (low) | | | |
| 0.50 (medium) | | | |
| 0.75 (high) | | | |

**Code:**
```python
for threshold in [0.25, 0.50, 0.75]:
    results = detector.predict(image, conf_threshold=threshold)
    # Count detections
```

**Questions:**

1. **Which threshold gives most detections?**
   ```

   ```

2. **Which threshold is safest for pedestrian detection? Why?**
   ```


   ```

3. **What is the risk of setting threshold too low?**
   ```


   ```

4. **What is the risk of setting threshold too high?**
   ```


   ```

---

## Part C: Failure Mode Analysis

### Task 4: Identify Detection Failures

For each image, identify and categorize failures:

**Failure Types:**
- **False Negative (FN):** Object exists but not detected
- **False Positive (FP):** Detection where no object exists
- **Misclassification (MC):** Wrong class label (e.g., bicycle detected as motorcycle)
- **Localization Error (LE):** Object detected but bounding box inaccurate

**Fill in the table:**

| Image | Failure Type | Example | Possible Cause |
|-------|--------------|---------|----------------|
| 1. Urban | | | |
| 2. Highway | | | |
| 3. Pedestrian | | | |
| 4. Night | | | |
| 5. Rain/Fog | | | |

**Example:**
```
Image: Night Scene
Failure Type: False Negative (FN)
Example: Pedestrian in dark clothing not detected
Possible Cause: Low contrast, insufficient training data for night scenes
```

---

### Task 5: Challenging Scenarios

Test YOLOv8 on these **challenging scenarios** (find or create test images):

1. **Partially occluded pedestrian** (behind tree, car)
   - Detected? Yes / No
   - Confidence:
   - Complete bounding box? Yes / No

2. **Pedestrian in unusual pose** (sitting, lying down, jumping)
   - Detected? Yes / No
   - Confidence:
   - Correct class? Yes / No

3. **Pedestrian with unusual appearance** (costume, full winter gear)
   - Detected? Yes / No
   - Confidence:

4. **Small pedestrian at distance** (> 50 meters)
   - Detected? Yes / No
   - Confidence:

5. **Cyclist (not bicycle class)**
   - Detected as? person / bicycle / motorcycle / not detected

**What do these failures tell you about training data?**
```


```

---

## Part D: Safety Implications

### Task 6: Define Safety Requirements

**Scenario:** You're designing a pedestrian detection system for **automatic emergency braking (AEB)**.

**Answer these questions:**

1. **What is more dangerous: False Positive or False Negative?**
   ```


   ```

2. **Define acceptable performance:**
   - Minimum recall (% of pedestrians detected):
   - Maximum false positive rate:
   - Minimum confidence threshold:

3. **What happens if:**
   - **False Negative:** Pedestrian not detected →
     ```

     ```
   - **False Positive:** Emergency brake for phantom object →
     ```

     ```

4. **Should you prioritize precision or recall for safety?**
   ```


   ```

---

## ✅ Self-Check

Before looking at solutions, verify:

- [ ] I can run object detection on images
- [ ] I understand what confidence scores mean
- [ ] I can explain precision-recall trade-off
- [ ] I've identified at least 5 failure modes
- [ ] I can set appropriate thresholds for safety-critical tasks
- [ ] I understand why different scenarios need different thresholds

---

## 💡 Discussion Questions

1. **Can you achieve 100% recall (detect all pedestrians) with zero false positives?**
   - Why or why not?

2. **How would you improve detection for night scenes?**
   - More training data?
   - Image preprocessing?
   - Sensor fusion (add LiDAR)?

3. **Is high confidence = correct detection?**
   - Can a system be confident and wrong?
   - Examples?

---

## 🔬 Advanced Challenge (Bonus)

### Task 7: Implement Precision-Recall Calculation

Write code to compute precision, recall, and F1 score:

```python
def compute_metrics(predictions, ground_truth, iou_threshold=0.5):
    """
    Compute precision, recall, F1

    Args:
        predictions: List of predicted boxes
        ground_truth: List of ground truth boxes
        iou_threshold: IoU threshold for matching

    Returns:
        precision, recall, f1
    """
    # TODO: Implement
    # Hint:
    # - Match predictions to ground truth using IoU
    # - Count true positives, false positives, false negatives
    # - Compute metrics

    pass

# Test your implementation
precision, recall, f1 = compute_metrics(predictions, ground_truth)
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1:.3f}")
```

**Solution:** See `solutions/exercise_3_solution.ipynb`

---

## 📊 Deliverables

Create a short report (1-2 pages) or presentation with:

1. **Detection results table** (all 5 images)
2. **Confidence threshold analysis** (with screenshots)
3. **Top 3 failure modes observed**
4. **Recommended threshold for pedestrian AEB system**
5. **Suggestions for improving detection performance**

---

## 📚 Additional Resources

- **COCO Evaluation Metrics:** https://cocodataset.org/#detection-eval
- **YOLOv8 Performance Benchmarks:** https://docs.ultralytics.com/models/yolov8/#performance
- **Precision-Recall Curves:** https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html

---

## ✏️ Solutions

Solution code and expected results: `solutions/exercise_3_solution.ipynb`

---

*Exercise created by Milin Patel | Hochschule Kempten*
*Last updated: 2025-01-17*
