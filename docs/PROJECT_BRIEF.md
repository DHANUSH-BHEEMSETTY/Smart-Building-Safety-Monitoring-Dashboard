# Smart Building Safety Monitoring Dashboard - Project Brief

This document serves as the single source of truth for the project. It outlines the scope, modules, datasets, and technology stack.

## 1. Project Overview
A unified dashboard that connects fire safety, security monitoring, and evacuation planning. Currently, these operate as disconnected systems. This project integrates them so that emergencies, like a fire alert, can automatically trigger a safe evacuation route without requiring manual cross-checking.

**Key Boundary:** Only a **fire event** triggers evacuation rerouting. **Suspicious activity** is alert-only.

## 2. Modules

### Module 1: Fire / Smoke Detection
*   **What it does:** Watches an uploaded video or stream and flags frames containing fire or smoke.
*   **How:** A YOLOv8 object detector (or a simpler CNN classifier) trained on a public fire/smoke image dataset.
*   **Datasets (Kaggle):**
    *   [Fire and Smoke Dataset for YOLOv8](https://www.kaggle.com/datasets/cubeai/fire-and-smoke-detection-for-yolov8)
    *   [Smoke-Fire-Detection-YOLO](https://www.kaggle.com/datasets/sayedgamal99/smoke-fire-detection-yolo)
    *   [Fire & Smoke Dataset – Object Detection, YOLO format](https://www.kaggle.com/datasets/azimjaan21/fire-and-smoke-dataset-object-detection-yolo)
    *   [Fire and Smoke Detection Dataset, 30k+ images](https://www.kaggle.com/datasets/hussainnasirkhan/fire-and-smoke-detection-dataset)

### Module 2: Suspicious Activity & Weapon Detection
*   **What it does:** Flags a person as "suspicious" based on explainable rules (e.g., detected in a restricted zone after a set time) and detects visible weapons (e.g., handguns, knives).
*   **How:** Reuses person-detection and zone-rule logic for restricted areas. Employs a trained object detector (YOLOv8 or RT-DETR) specifically for identifying weapons.
*   **Datasets (Kaggle):**
    *   **Person Detection:**
        *   [People Detection Dataset](https://www.kaggle.com/datasets/adilshamim8/people-detection)
        *   [Human Detection Dataset – CCTV footage](https://www.kaggle.com/datasets/constantinwerner/human-detection-dataset)
    *   **Weapon Detection:**
        *   [Weapons Detection Dataset (Pistols/Knives)](https://www.kaggle.com/datasets/mralhasan/weapons-detection-dataset)
        *   [Handgun Detection Dataset](https://www.kaggle.com/datasets/andrewmvd/handgun-detection)
        *   [Weapon (Gun/Knife) Dataset for YOLO](https://www.kaggle.com/datasets/kshitij192/pistol-dataset)

### Module 3: Evacuation Route Suggestion
*   **What it does:** Once a fire is detected, suggests the safest evacuation route avoiding the affected area.
*   **How:** The building floor plan is represented as a graph (nodes = rooms/corridors, edges = doorways/hallways) using NetworkX. When a room is blocked by fire, A*/Dijkstra pathfinding is rerun to find the next-best route.
*   **Dataset:** No dataset needed. Uses a hand-drawn mock diagram (6-8 rooms/corridors) encoded directly as a graph.

## 3. Technology Stack
*   **Language:** Python
*   **Backend:** FastAPI (Serves all three modules through one API)
*   **Dashboard / UI:** Streamlit
*   **Video Handling:** OpenCV (Frame-by-frame video processing)
*   **Evacuation Routing:** NetworkX + A*/Dijkstra
*   **Detection Models:** YOLOv8 (Ultralytics) or simple CNN
*   **Visualization:** Matplotlib / Streamlit charts (Overlaying evacuation paths)

## 4. Scope Boundaries & Clarifications
To keep expectations honest and matched to what is actually being built:
*   **Integration over Invention:** This is not a single, unified AI model. It consists of separate, simpler models combined with rules and pathfinding layers integrated into one pipeline.
*   **Demo Environment:** This is not a live, multi-camera, real-time system. The demo runs on a single video feed using pre-recorded test clips.
*   **Mock Environment:** The floor plan is a simplified mock building, not a real architectural blueprint.
*   **Performance Metrics:** Detection accuracy and false-positive rates will be measured and reported separately for each module, rather than as a single combined metric.

## 5. Model Comparison (Fire & Smoke Detection)

Based on Kaggle training results and local benchmarks, the following compares various models for the Fire/Smoke detection module:

| Metric | YOLOv8n | YOLOv11n | YOLO26n | RT-DETR-L |
| :--- | :--- | :--- | :--- | :--- |
| **mAP50** | 0.7089 | 0.7073 | 0.6804 | 0.7059 |
| **mAP50-95** | 0.4017 | 0.3976 | 0.3813 | 0.3931 |
| **Parameters** | ~3.2M | 2.58M | ~2.37M | 31.9M |
| **Weights Size** | 6.2 MB | 5.4 MB | ~5.3 MB | 66.2 MB |
| **Training Epochs** | 15 | 15 | 15 | 15 |

*\*Note: All models were trained for a full 15 epochs on Kaggle T4 GPUs.*

**Conclusion:** All YOLO variants performed similarly well, with YOLOv8n and YOLOv11n having nearly identical mAP scores (0.7089 vs 0.7073). YOLOv11n remains highly recommended due to its updated architecture, faster inference, and slightly smaller memory footprint. RT-DETR-L also performed well but its massive size (66.2 MB) and slower inference makes it less ideal for real-time webcam processing.
