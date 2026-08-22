# Capstone Project: Weekly Progress Report - Week 1

## Project Details
**Project Title:** Smart Building Safety Monitoring Dashboard
**Week Number:** 1
**Date:** [Insert Date]
**Team Members:** [Insert Names and Registration Numbers]
**Faculty Guide:** [Insert Guide's Name]

---

## 1. Objectives for Week 1
The primary goal for the first week was to establish the project scope, finalize the foundational architecture, and set up the development environment. We also aimed to initialize the core modules, specifically porting over the pre-existing person detection logic.

## 2. Tasks Completed This Week

### 2.1 Project Scoping & Documentation
*   **Finalized Requirements:** Clearly defined the boundaries of the project (e.g., distinguishing between fire alerts triggering evacuation vs. suspicious activity being alert-only).
*   **Documentation:** Created the `PROJECT_BRIEF.md` and `First_Review_Scoping_Document.docx` to serve as the single source of truth for the project's features and datasets.

### 2.2 Environment & Repository Setup
*   **Directory Structure:** Established a modular architecture for the repository, including dedicated directories for `backend`, `dashboard`, `data`, and `modules` (`fire_detection`, `suspicious_activity`, `evacuation_routing`).
*   **Dependencies:** Identified the core technology stack (FastAPI, Streamlit, NetworkX, Ultralytics YOLOv8, OpenCV) and initialized the `requirements.txt` file.

### 2.3 Module Initialization (Suspicious Activity)
*   **Code Integration:** Successfully integrated the YOLOv8 person-detection script (`detection.py`) and zone-rule logic (`rules.py`) adapted from our previous restricted-area monitoring project.
*   **Model Preparation:** Downloaded the pre-trained `yolov8n.pt` model weights and sample testing footage (`testing video.mp4`) to facilitate immediate local testing.
*   **Testing Setup:** Created an initial `test_module.py` to validate the zone rules and bounding box logic before full backend integration.

---

## 3. Challenges Encountered & Resolutions
*   *Challenge:* Determining the best way to handle real-time video processing across multiple modules without significant lag.
*   *Resolution:* Decided to use a single FastAPI backend to serve inferences, decoupling the heavy YOLOv8 processing from the Streamlit frontend. 

---

## 4. Plan for Week 2
Moving into the second week, the focus will shift towards implementing the remaining core algorithms and preparing the datasets:
1.  **Evacuation Routing:** Develop and test the graph-based pathfinding logic (A*/Dijkstra) using NetworkX on a mock building floor plan.
2.  **Fire/Smoke Detection:** Download the selected Kaggle fire/smoke datasets, format them correctly in `data.yaml`, and write the initial YOLOv8 training script.
3.  **Backend Prototyping:** Begin scaffolding the FastAPI application to link the Suspicious Activity module outputs to API endpoints.

---
**Faculty Comments / Feedback:**

*(Space for Guide's Remarks)*

<br><br><br>
**Signature of Guide:** _______________________
