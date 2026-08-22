# Real-Time Restricted Area Monitoring System

Welcome to the documentation for the **Real-Time Restricted Area Monitoring System**. This capstone project integrates computer vision, real-time routing algorithms, and instant messaging APIs into a unified security dashboard.

## System Architecture

The system consists of several independent modules wired together through a FastAPI backend and visualized via a Streamlit dashboard.

### 1. Fire & Smoke Detection (`modules/fire_detection/`)
- Uses a YOLOv8 model fine-tuned on fire and smoke datasets.
- Implements a **persistence filter** requiring fire to be detected across multiple consecutive frames (e.g., 8 out of the last 10 frames) to eliminate false positives.
- Estimates fire severity based on bounding box area percentages, ignoring minor/brief flames.
- Includes a benchmarking suite (`model_comparison/`) that dynamically evaluates different YOLO architectures to configure the best-performing weights.

### 2. Suspicious Activity & Weapon Detection (`modules/suspicious_activity/`)
- Detects persons entering restricted zones using configurable polygons in `zone_config.json`.
- Enforces time-based access control rules (e.g., triggering alerts if someone enters Zone A after 21:00).
- Features a completely independent **Weapon Detection** pipeline fine-tuned on a Kaggle dataset to detect guns and knives, triggering dedicated high-priority alerts.

### 3. Evacuation Routing (`modules/evacuation_routing/`)
- Dynamically models the building's floor plan as a graph using `NetworkX`.
- When a fire is confirmed, it calculates the most feasible escape route starting from the fire's origin room.
- Routes intelligently avoid blocked zones and generate visual floor plan diagrams using `Matplotlib`.

### 4. Notifications (`modules/notifications/`)
- Seamlessly integrates with the Telegram Bot API to push instant notifications directly to a smartphone.
- Distinguishes between event types (e.g., `fire`, `suspicious_activity`, `weapon_detected`) and passes exact timestamps and location details.
- See `modules/notifications/README.md` for instructions on configuring your API tokens.

### 5. Dashboard & Backend (`dashboard/` & `backend/`)
- **FastAPI Backend:** Orchestrates all inference modules, exposes endpoints like `/analyze-frame` and `/evacuation-route`, and handles the Telegram notification triggers.
- **Streamlit Dashboard:** Provides a real-time UI that processes video feeds, displays current statuses, pops up critical alert banners, confirms security dispatch, and renders live evacuation routes.

---

## Quick Start Guide

### 1. Configure Notifications
Before starting the system, configure your Telegram credentials to receive alerts. Follow the instructions in `modules/notifications/README.md` and insert your tokens into `telegram_bot.py`.

### 2. Start the Backend Server
Navigate to the `backend` directory and start the FastAPI server:
```bash
cd backend
python -m uvicorn main:app --reload
```

### 3. Start the Dashboard
In a new terminal window, navigate to the `dashboard` directory and launch Streamlit:
```bash
cd dashboard
python -m streamlit run app.py
```

Open your browser to `http://localhost:8501`. You can upload any security footage into the sidebar to see the automated monitoring and alerting pipeline in action!
