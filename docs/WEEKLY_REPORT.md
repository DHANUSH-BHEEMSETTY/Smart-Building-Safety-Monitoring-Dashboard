# Weekly Progress Report: Smart Building Safety Monitoring Dashboard

## 1. Executive Summary
This week's focus was primarily on preparing the core datasets and conducting initial training and benchmarking for the **Fire / Smoke Detection** module. Since training deep learning models is time-intensive, we utilized Kaggle's T4 GPUs to train multiple model architectures over the week to determine the most efficient model for our real-time processing constraints.

## 2. Dataset Preparation & Details

### Dataset 1: Fire & Smoke Detection
- **Name:** `Smoke-Fire-Detection-YOLO` (Kaggle: sayedgamal99)
- **Classes:** 2 (`smoke`, `fire`)
- **Total Images:** 21,527
- **Splits:**
  - **Training:** 14,122 images (65.6%)
  - **Validation:** 3,099 images (14.4%)
  - **Testing:** 4,306 images (20.0%)
- **Status:** Extracted, preprocessed, and actively used for model training this week.

### Dataset 2: Suspicious Activity & Weapon Detection
- **Name:** `Weapon Detection Dataset (YOLO Optimized)` (Kaggle: alinoorqureshi)
- **Status:** Data has been successfully downloaded and extracted into structured train, validation, and test splits. Training on this dataset is queued for the upcoming week following the successful benchmarking of our baseline models.

## 3. Model Comparison & Training Findings (Fire/Smoke Detection)

We trained four different object detection architectures for a baseline of 15 epochs to compare performance, size, and real-time viability.

| Model | mAP@50 | mAP@50-95 | Weights Size | Parameters |
| :--- | :--- | :--- | :--- | :--- |
| **YOLOv8n** | 0.7089 | 0.4017 | 6.2 MB | ~3.2M |
| **YOLOv11n** | 0.7073 | 0.3976 | 5.4 MB | 2.58M |
| **YOLO26n** | 0.6804 | 0.3813 | 5.3 MB | ~2.37M |
| **RT-DETR-L** | 0.7059 | 0.3931 | 66.2 MB | 31.9M |

### Key Findings & Conclusion:
1. **Performance Parity**: All models adapted quickly, showing solid mAP scores within just 15 epochs of training. YOLOv8n achieved a marginally higher mAP@50 (0.7089) compared to the others.
2. **Speed & Size Considerations**: While RT-DETR-L performed well (mAP@50: 0.7059), its massive weight size (66.2 MB) and significantly slower inference time make it impractical for our real-time dashboard requirements.
3. **Recommended Model**: **YOLOv11n** is the recommended choice. Despite a negligible drop in mAP compared to YOLOv8n, it offers a great balance of speed, modern architecture, and a smaller memory footprint (5.4 MB vs 6.2 MB).

## 4. Next Steps for Next Week
- **Extended Training:** Queue a 30–40 epoch training run for the chosen **YOLO11n** architecture on Kaggle to generate converged, production-ready weights.
- **Weapon Detection Module:** Initiate fine-tuning on the extracted Weapon Detection dataset using YOLO11n.
- **Dashboard UI & UX Enhancement:** Design and polish the frontend dashboard (Streamlit) and FastAPI backend endpoints for smooth real-time video streaming, interactive alerts, and responsive metrics display.
- **Evacuation Routing Integration:** Finalize the mock floor plan graph using NetworkX and connect dynamic rerouting to fire detection trigger events.

