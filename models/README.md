# Trained Model Weights

This directory contains the fine-tuned YOLOv11 model weights used by the Smart Building Safety Monitoring Dashboard.

## Required Files

| File | Source Notebook | Task | Classes |
|---|---|---|---|
| `yolo11n_fire_smoke_best.pt` | `yolo-v11-fully-trained.ipynb` / `yolo_v11_smoke and fire.ipynb` | Smoke & Fire Detection | smoke, fire |
| `yolo11n_weapon_best.pt` | `yolov11-weapon-detection.ipynb` | Weapon Detection | gun, knife |

## How to Obtain & Place Weights

1. Open your Kaggle notebook output for each training run.
2. Download the `best.pt` file from the output ZIP archive (e.g. `yolo11n_30ep_results.zip` or `yolo11n_weapon_results.zip`).
3. Rename and place them directly in this directory (`models/`) with the filenames shown above.

---

## Model Benchmark & Evaluation Summary

Both models were trained on Kaggle utilizing dual NVIDIA Tesla T4 GPUs with the YOLOv11n (nano) architecture for 30 epochs at 640×640 image resolution.

### 1. Smoke & Fire Detection Model (`yolo11n_fire_smoke_best.pt`)
- **Dataset:** `sayedgamal99/smoke-fire-detection-yolo` (3,094 validation images, 3,917 instances)
- **Classes:** `['smoke', 'fire']` (nc: 2)
- **Epochs:** 30
- **Overall Metrics:**
  - **mAP@50:** **74.78%** (`0.7478`)
  - **mAP@50-95:** **42.83%** (`0.4283`)
  - **Precision:** **74.30%** (`0.7430`)
  - **Recall:** **68.21%** (`0.6821`)
- **Per-Class Metrics:**
  - **Smoke:** Precision: **79.90%** | Recall: **73.00%** | mAP@50: **80.70%** | mAP@50-95: **49.50%**
  - **Fire:** Precision: **68.70%** | Recall: **63.40%** | mAP@50: **68.90%** | mAP@50-95: **36.10%**
- **Average Inference Latency:** **19.24 ms/frame** (~52 FPS)

### 2. Weapon Detection Model (`yolo11n_weapon_best.pt`)
- **Dataset:** `alinoorqureshi/weapon-detection-yolo-optimized` (4,544 validation images, 5,935 instances)
- **Classes:** `['gun', 'knife']` (nc: 2)
- **Epochs:** 30
- **Overall Metrics:**
  - **mAP@50:** **77.43%** (`0.7743`)
  - **mAP@50-95:** **46.86%** (`0.4686`)
  - **Precision:** **83.67%** (`0.8367`)
  - **Recall:** **69.12%** (`0.6912`)
- **Average Inference Latency:** **19.40 ms/frame** (~51.5 FPS)
