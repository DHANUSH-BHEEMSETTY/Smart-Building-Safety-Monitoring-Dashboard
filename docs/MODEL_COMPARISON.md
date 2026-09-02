# Model Comparison & Fine-Tuning Benchmarks (Kaggle Training)

## 1. Fire / Smoke Detection Benchmark (15 Epochs Initial Screening)

Trained on the Fire & Smoke dataset (`sayedgamal99/smoke-fire-detection-yolo`) using Kaggle T4 GPUs:

| Model | mAP@50 | mAP@50-95 | Notes |
| :--- | :--- | :--- | :--- |
| **YOLOv8n** | 0.7089 | 0.4017 | Baseline CNN architecture |
| **YOLOv11n** | 0.7073 | 0.3976 | Modernized backbone & C3k2/C2PSA blocks |
| **YOLO26n** | 0.6804 | 0.3813 | Experimental |
| **RT-DETR-L** | 0.7059 | 0.3931 | Real-Time Detection Transformer |

---

## 2. Selected Models — Full 30-Epoch Fine-Tuning Results (`yolo-v11-fully-trained.ipynb`)

Based on architectural efficiency, real-time FPS throughput (~52 FPS), and ease of edge deployment, **YOLOv11n** was selected and trained for 30 epochs on both safety hazard tasks.

### Fire & Smoke Detection (YOLOv11n — 30 Epochs)
- **Source Notebook:** `yolo-v11-fully-trained.ipynb`
- **Dataset:** `sayedgamal99/smoke-fire-detection-yolo` (3,094 val images, 3,917 instances)
- **Overall mAP@50:** **0.7478** (+4.05% improvement over 15-epoch screening)
- **Overall mAP@50-95:** **0.4283** (+3.07% improvement over 15-epoch screening)
- **Precision:** **0.7430**
- **Recall:** **0.6821**
- **Per-Class Breakdown:**
  - **Smoke:** Precision: **79.9%** | Recall: **73.0%** | mAP@50: **80.7%** | mAP@50-95: **49.5%**
  - **Fire:** Precision: **68.7%** | Recall: **63.4%** | mAP@50: **68.9%** | mAP@50-95: **36.1%**
- **Inference Speed:** **19.24 ms/frame** (~52 FPS)

### Weapon Detection (YOLOv11n — 30 Epochs)
- **Source Notebook:** `yolov11-weapon-detection.ipynb`
- **Dataset:** `alinoorqureshi/weapon-detection-yolo-optimized` (4,544 val images, 5,935 instances)
- **Overall mAP@50:** **0.7743**
- **Overall mAP@50-95:** **0.4686**
- **Precision:** **0.8367**
- **Recall:** **0.6912**
- **Inference Speed:** **19.40 ms/frame** (~51.5 FPS)
