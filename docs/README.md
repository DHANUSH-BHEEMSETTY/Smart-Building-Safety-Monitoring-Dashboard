# SmartBuildAI — Intelligent Safety & Evacuation Command Center

Welcome to the technical documentation for **SmartBuildAI**. This capstone project integrates real-time computer vision (YOLOv11), dynamic graph pathfinding (`NetworkX`), and security alerting into a unified pipeline.

---

## Project Structure & File Map

```text
capstone/
├── backend/
│   └── main.py                     ✅ FastAPI backend orchestrating multi-frame temporal fire filtering, weapon detection & routing
│
├── dashboard/
│   └── app.py                      ✅ Streamlit UI with live webcam stream, video upload, dynamic route display & alert feeds
│
├── modules/
│   ├── fire_detection/
│   │   ├── inference.py            ✅ YOLOv11 loader + FireAlertManager (sustained 6-frame detection, conf ≥ 0.60)
│   │   ├── train.py                ✅ YOLOv11n 30-epoch training pipeline
│   │   ├── test_filter.py          ✅ Verified: 4 temporal scenarios tested & passing (false alerts eliminated)
│   │   └── download_dataset.py     ✅ Fire/smoke dataset downloader
│   │
│   ├── suspicious_activity/
│   │   ├── detection.py            ✅ Person (COCO) + YOLOv11 Weapon loader (conf ≥ 0.65, class names)
│   │   ├── rules.py                ✅ Zone & restricted hours evaluation engine
│   │   ├── train_weapon_model.py   ✅ YOLOv11n 30-epoch training pipeline
│   │   ├── test_weapon.py          ✅ Verified: Alert format with bounding box & confidence
│   │   └── zone_config.json        ✅ Server room & Lobby after-hours polygons
│   │
│   ├── evacuation_routing/
│   │   ├── floor_plan.py           ✅ NetworkX graph model + Dijkstra/A* pathfinding avoiding fire nodes
│   │   └── route_*.png             ✅ Generated floor plan visualizations
│   │
│   └── notifications/
│       └── telegram_bot.py         ✅ Security alert dispatch via Telegram API
│
├── models/
│   ├── README.md                   ✅ Instructions & exact benchmark metrics (74.78% mAP Fire, 77.43% mAP Weapon)
│   ├── yolo11n_fire_smoke_best.pt  ✅ Fine-tuned YOLOv11 Fire/Smoke weights (Installed & Validated)
│   └── yolo11n_weapon_best.pt      ✅ Fine-tuned YOLOv11 Weapon weights (Installed & Validated)
│
├── docs/
│   ├── MODEL_COMPARISON.md         ✅ Complete 15-epoch screening vs 30-epoch fine-tuning benchmark documentation
│   ├── PROJECT_BRIEF.md            ✅ Project scoping & architecture documentation
│   ├── Review_1_Presentation.md    ✅ Review slide deck
│   └── WEEKLY_REPORT.md            ✅ Progress reports
│
├── yolo-v11-fully-trained.ipynb    ✅ 30-Epoch Fire/Smoke Kaggle notebook (74.78% mAP50, 19.24 ms latency)
├── yolov11-weapon-detection.ipynb  ✅ 30-Epoch Weapon Kaggle notebook (77.43% mAP50, 19.40 ms latency)
├── requirements.txt                ✅ Project dependencies list
└── testing video.mp4               ✅ Local sample test video
```

---

## System Architecture

The system consists of several independent modules wired together through a FastAPI backend and visualized via a Streamlit dashboard.

### 1. Fire & Smoke Detection (`modules/fire_detection/`)
- Uses fine-tuned **YOLOv11n** (`models/yolo11n_fire_smoke_best.pt`) with fallback to YOLOv8.
- Implements **`FireAlertManager`** multi-frame temporal persistence (requiring 6 out of 10 consecutive positive frames or large area coverage ≥ 5%) to eliminate false positives on live webcam feeds.
- Classifies into `NORMAL`, `MINOR_LOW_SEVERITY` (logged only), and `FULL_ALERT` (triggers security notifications and evacuation rerouting).

### 2. Suspicious Activity & Weapon Detection (`modules/suspicious_activity/`)
- Detects persons entering restricted zones using configurable polygons in `zone_config.json`.
- Enforces time-based access control rules (e.g., triggering alerts if someone enters Zone A after 21:00).
- Features a fine-tuned **YOLOv11 Weapon Detection** pipeline (conf ≥ 0.65) to detect guns and knives, triggering dedicated high-priority alerts with class names.

### 3. Evacuation Routing (`modules/evacuation_routing/`)
- Dynamically models the building's floor plan as a graph using `NetworkX`.
- When a fire is confirmed, it calculates the shortest-safe escape route starting from the fire's origin room.
- Routes intelligently avoid blocked hazard nodes and generate visual floor plan diagrams using `Matplotlib`.

### 4. Notifications (`modules/notifications/`)
- Seamlessly integrates with the Telegram Bot API to push instant notifications directly to a smartphone.
- Distinguishes between event types (e.g., `fire`, `suspicious_activity`, `weapon_detected`) and passes exact timestamps and location details.

### 5. Dashboard & Backend (`dashboard/` & `backend/`)
- **FastAPI Backend:** Orchestrates all inference modules, exposes endpoints (`/analyze-frame`, `/evacuation-route`), and handles security dispatch.
- **Streamlit Dashboard:** Provides a real-time UI that processes video feeds/live webcam, displays current statuses, pops up critical alert banners, confirms security dispatch, and renders live evacuation routes.

---

## Quick Start Guide

### 1. Start the Backend Server
```bash
uvicorn backend.main:app --reload --port 8000
```

### 2. Start the Dashboard
```bash
streamlit run dashboard/app.py
```

Navigate to `http://localhost:8501`.
