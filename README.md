# SmartBuildAI — Intelligent Safety & Evacuation Command Center

A unified AI-powered command center that connects fire safety, security monitoring, and dynamic evacuation planning into a single automated pipeline.

Emergencies (such as confirmed fire hazards or weapon threats) automatically trigger instant security alerts and dynamic, obstruction-free evacuation route generation without requiring manual cross-checking.

---

## Project Structure & Module Overview

```text
capstone/
├── backend/
│   └── main.py                     ✅ FastAPI backend orchestrating multi-frame temporal fire filtering, weapon detection & routing
│
├── dashboard/
│   └── app.py                      ✅ Modern Streamlit Command Center UI (real-time video, multi-camera matrix, alerts & evacuation map)
│
├── modules/
│   ├── fire_detection/
│   │   ├── inference.py            ✅ YOLOv11 loader + FireAlertManager (6-frame sliding window, conf ≥ 0.35, area ≥ 2.0%)
│   │   ├── train.py                ✅ YOLOv11n 30-epoch training pipeline
│   │   ├── test_filter.py          ✅ Verified: 4 temporal scenarios tested & passing (false alerts eliminated)
│   │   └── download_dataset.py     ✅ Fire/smoke dataset downloader
│   │
│   ├── suspicious_activity/
│   │   ├── detection.py            ✅ Person (COCO) + YOLOv11 Weapon loader (conf ≥ 0.50, gun/knife classes)
│   │   ├── rules.py                ✅ Zone & restricted hours evaluation engine
│   │   ├── train_weapon_model.py   ✅ YOLOv11n 30-epoch training pipeline
│   │   ├── test_weapon.py          ✅ Verified: Alert format with bounding box & confidence
│   │   └── zone_config.json        ✅ Server room & Lobby after-hours polygons
│   │
│   ├── evacuation_routing/
│   │   ├── floor_plan.py           ✅ NetworkX graph model + Dijkstra/A* pathfinding avoiding fire nodes (dark-theme renderer)
│   │   └── route_*.png             ✅ Generated floor plan visualizations
│   │
│   └── notifications/
│       ├── telegram_notifier.py    ✅ python-dotenv loader, 60s rate-limiting & structured security alert dispatch
│       ├── telegram_bot.py         ✅ Legacy import facade for backward compatibility
│       └── test_telegram.py        ✅ Standalone bot credential & dispatch verification script
│
├── models/
│   ├── README.md                   ✅ Benchmark documentation (74.78% mAP Fire, 77.43% mAP Weapon)
│   ├── yolo11n_fire_smoke_best.pt  ✅ Fine-tuned YOLOv11 Fire/Smoke weights (5.19 MB, Installed & Validated)
│   └── yolo11n_weapon_best.pt      ✅ Fine-tuned YOLOv11 Weapon weights (5.22 MB, Installed & Validated)
│
├── docs/
│   ├── MODEL_COMPARISON.md         ✅ Complete 15-epoch screening vs 30-epoch fine-tuning benchmark documentation
│   ├── PROJECT_BRIEF.md            ✅ Project scoping & architecture documentation
│   ├── Review_1_Presentation.md    ✅ Review slide deck
│   └── WEEKLY_REPORT.md            ✅ Progress reports
│
├── .env.example                    ✅ Template for Telegram bot credentials
├── requirements.txt                ✅ Project dependencies list
└── testing video.mp4               ✅ Local sample test video
```

---

## False Alarm Mitigation & Temporal Filtering (`FireAlertManager`)

In real-world surveillance, single-frame object detection produces false alarms from cigarette lighters, matchsticks, reflections, and transient optical glitches. **SmartBuildAI** employs a **2-tier temporal filtering architecture** (`modules/fire_detection/inference.py`) to eliminate false positives before any alert or evacuation is dispatched.

```
                          Raw YOLOv11 Detections
                                    │
                                    ▼
                     ┌──────────────────────────────┐
                     │   FireAlertManager Filter    │
                     │  (6-Frame Sliding Window)    │
                     └──────────────┬───────────────┘
                                    │
              ┌─────────────────────┴─────────────────────┐
              ▼                                           ▼
   Brief / Small Flicker                       Sustained / Large Fire
   • Lighter / match (< 3 frames)              • Fire persists ≥ 3 of 6 frames, OR
   • Flame area < 2.0% of screen               • Flame area ≥ 2.0% of screen
              │                                           │
              ▼                                           ▼
      [MINOR_LOW_SEVERITY]                          [FULL_ALERT]
      ❌ 0 Telegram alerts                         🚨 Telegram alert dispatched
      ❌ 0 Evacuation routing                      🗺️ Dynamic escape route generated
      ℹ️ Subtle log in UI only                    ⚠️ Critical emergency UI card
```

### 3-Tier Classification Engine:

| Status Tier | Criteria | System Action |
|---|---|---|
| **`NORMAL`** | Zero smoke/flame detections across sliding window | Normal surveillance, status bar green. |
| **`MINOR_LOW_SEVERITY`** | Brief spark or flame detected in $<3$ frames with area $<2.0\%$ | Logged in UI only. **0 Telegram alerts sent, 0 evacuation routes triggered.** |
| **`FULL_ALERT`** | Flame persists for $\ge 3$ frames within a 6-frame window, **OR** flame area $\ge 2.0\%$ | **Telegram notification dispatched** to security, **evacuation route generated**, critical UI card rendered. |

---

### Empirical Validation: 4 Tested Real-World Scenarios

The temporal filtering engine was evaluated against 4 real-world edge-case scenarios via `modules/fire_detection/test_filter.py`:

| Test Scenario | Detection Pattern | System Decision | Verification Result |
|---|---|---|---|
| **1. Brief Lighter / Match Flick** | Flame detected in 2 frames only (0.5% screen area) | `MINOR_LOW_SEVERITY` $\rightarrow$ `NORMAL` | ✅ **Passed:** 0 Telegram alerts, 0 sirens. Automatically dropped on frame 4. |
| **2. Intermittent Glare / Glitch** | Single isolated detection every 4 frames | `MINOR_LOW_SEVERITY` $\rightarrow$ `NORMAL` | ✅ **Passed:** Filter prevents isolated glitch frames from accumulating. |
| **3. Real Fire Outbreak** | Growing flame covering $\ge 2.0\%$ screen area | `FULL_ALERT` (Immediate) | ✅ **Passed:** Instant alert dispatch on Frame 1 without waiting for window to fill. |
| **4. Small Flame Becoming Sustained** | Small flame (0.5% area) persisting for 3+ frames | `MINOR` $\rightarrow$ `FULL_ALERT` | ✅ **Passed:** Escalates to emergency alert once confirmed sustained and growing. |

---

## Telegram Security Notification Pipeline

Security personnel receive instant, formatted notifications via Telegram when genuine incidents are confirmed.

### Configuration (`.env`):
Credentials are loaded at startup using `python-dotenv`:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHAT_ID=your_chat_id
```

### Key Safety & Reliability Features:
1. **60-Second In-Memory Rate Limiting:** Duplicate alerts for the same `(alert_type, location)` pair within a 60-second window are suppressed to prevent spamming security teams while a hazard is continuously tracked.
2. **Distractor Object Filtering:** Common false-alert items (smartphones, cards, wallets, badges) produce **0 alerts** because the weapon detector is specifically fine-tuned for `gun` and `knife` classes.
3. **Structured Alert Messages:**
   - **🔥 Fire:** `🚨 EMERGENCY FIRE & SMOKE ALERT 🚨` (Zone, timestamp, confidence, evacuation route notice).
   - **⚔️ Weapon:** `🚨 LETHAL THREAT: WEAPON DETECTED 🚨` (Identified weapon class, confidence, dispatch protocol).
   - **⚠️ Suspicious Activity:** `⚠️ SECURITY ALERT: SUSPICIOUS ACTIVITY ⚠️` (Zone, timestamp, rule infraction details).

---

## Dynamic Evacuation Routing Subsystem

When a sustained fire is verified:
1. The **FastAPI backend** marks the fire origin room/zone as impassable (`blocked_rooms`).
2. **`NetworkX`** calculates the optimal, obstacle-free escape path to the closest safe exit using Dijkstra's shortest-path algorithm.
3. A high-contrast floor plan graph diagram is dynamically rendered and delivered to the dashboard interface.

---

## Model Benchmark Summary (30-Epoch Fine-Tuning)

| Task | Architecture | Dataset | mAP@50 | mAP@50-95 | Precision | Recall | Inference Latency |
|---|---|---|---|---|---|---|---|
| **Smoke & Fire** | YOLOv11n | `sayedgamal99/smoke-fire-detection-yolo` | **74.78%** | **42.83%** | **74.30%** | **68.21%** | **19.24 ms** (~52 FPS) |
| **Weapon Detection** | YOLOv11n | `alinoorqureshi/weapon-detection-yolo-optimized` | **77.43%** | **46.86%** | **83.67%** | **69.12%** | **19.40 ms** (~51.5 FPS) |

---

## How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Telegram (Optional for Alerts)
Copy `.env.example` to `.env` and fill in your Bot Token and Chat ID:
```bash
cp .env.example .env
```
Test the notification setup with:
```bash
python modules/notifications/test_telegram.py
```

### 3. Start the FastAPI Backend
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### 4. Start the SmartBuildAI Command Center
```bash
streamlit run dashboard/app.py
```

Navigate to **`http://localhost:8501`** in your browser to access the command center.

---

## Datasets

- **Fire & Smoke:** [Smoke-Fire-Detection-YOLO (Kaggle)](https://www.kaggle.com/datasets/sayedgamal99/smoke-fire-detection-yolo)
- **Weapon Detection:** [Weapon Detection Dataset (Kaggle)](https://www.kaggle.com/datasets/alinoorqureshi/weapon-detection-yolo-optimized)
