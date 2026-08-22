# Smart Building Safety Monitoring Dashboard

A unified dashboard that connects fire safety, security monitoring, and evacuation planning. Currently, these operate as disconnected systems. This project integrates them so that emergencies, like a fire alert, can automatically trigger a safe evacuation route without requiring manual cross-checking.

## Modules

### 1. Fire / Smoke Detection
Watches an uploaded video or live stream and flags frames containing fire or smoke using a trained YOLO model.

### 2. Suspicious Activity & Weapon Detection
Flags a person as "suspicious" based on explainable rules (e.g., detected in a restricted zone after a set time) and detects visible weapons (e.g., handguns, knives).

### 3. Evacuation Route Suggestion
Once a fire is detected, suggests the safest evacuation route avoiding the affected area using NetworkX graphs and A*/Dijkstra pathfinding on the building floor plan.

## Technology Stack
- **Language**: Python
- **Backend**: FastAPI
- **Frontend/Dashboard**: Streamlit (`streamlit-webrtc` for live webcam)
- **Computer Vision**: OpenCV, Ultralytics YOLO
- **Routing**: NetworkX

## How to Run Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the FastAPI Backend**:
   Open a terminal and run:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```
3. **Start the Streamlit Dashboard**:
   Open a second terminal and run:
   ```bash
   streamlit run dashboard/app.py
   ```
   Navigate to `http://localhost:8501` to use the dashboard!

## Datasets

> **Note:** Datasets are not included in this repository due to size. Download them from the links below and place them according to the paths expected in each module's `data.yaml` / config before training.

### Fire/Smoke Detection
- **Smoke-Fire-Detection-YOLO** (Kaggle) — [https://www.kaggle.com/datasets/sayedgamal99/smoke-fire-detection-yolo](https://www.kaggle.com/datasets/sayedgamal99/smoke-fire-detection-yolo)

### Weapon Detection
- **Weapon Detection Dataset** (Kaggle) — [https://www.kaggle.com/datasets/alinoorqureshi/weapon-detection-yolo-optimized](https://www.kaggle.com/datasets/alinoorqureshi/weapon-detection-yolo-optimized)
