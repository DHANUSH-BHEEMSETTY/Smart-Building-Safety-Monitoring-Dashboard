### Slide 1: TITLE SLIDE
**Smart Building Safety Monitoring Dashboard**

**Team Members:** 
- B. Mahitha — 23BCE9076
- B. Dhanush — 23BCE9640
- O. Mounika — 23BCE20018
- E. Veda Sree — 23BCE7084

**Under the Guidance of:**
- Mr. Kandru Lakshmi Sai Praneeth

**Department:** [CSE]
**University:** [VIT-AP]

***

### Slide 2: ABSTRACT
Current building safety protocols rely heavily on disconnected systems for fire detection, security monitoring, and evacuation planning. This separation requires manual cross-checking during emergencies, causing critical delays. Our project proposes a Smart Building Safety Monitoring Dashboard that integrates these functions into a unified pipeline. By combining computer vision for real-time hazard detection with dynamic graph-based pathfinding, the system automatically triggers safe evacuation routes upon verifying a fire, thereby reducing response times and improving occupant safety.

***

### Slide 3: PROBLEM STATEMENT
Currently, fire safety, security monitoring, and evacuation planning operate as completely disconnected systems in most facilities. When an emergency such as a fire occurs, personnel must manually cross-reference camera feeds, alarm locations, and building maps to direct people safely. This introduces severe delays and the potential for human error. Furthermore, static evacuation routes may unwittingly direct occupants toward unseen hazards. There is a critical need for a unified system that synthesizes threat detection and dynamic evacuation planning to guarantee an immediate, safe response without manual intervention.

***

### Slide 4: OBJECTIVES
**Main Objective:** 
To develop a unified Smart Building Safety Monitoring Dashboard that integrates hazard detection and dynamic evacuation planning into a single automated pipeline, prioritizing transformer-based visual detection models.

**Specific Objectives:**
1. Develop Fire/Smoke and Suspicious Activity modules transitioning toward Vision Transformer models for improved context awareness.
2. Implement zone-based rules to flag security breaches.
3. Create an Evacuation Route Suggestion module using A*/Dijkstra algorithms and NetworkX to calculate the safest paths dynamically.
4. Integrate all modules via a FastAPI backend to ensure a fire event automatically triggers evacuation rerouting.
5. Provide a centralized Streamlit dashboard for real-time visualization and alerting.

***

### Slide 5: LITERATURE REVIEW & RESEARCH GAP

**Fire/Smoke Detection:** Recent studies demonstrate the efficacy of deep learning in early fire detection. While optimized architectures like YOLOv8n and YOLOv5 have been adapted for indoor environments (MDPI, 2024; PMC, 2025), newer approaches seek better contextual understanding.

**Weapon & Suspicious Activity Detection:** AI-based surveillance utilizing deep learning enables robust anomaly detection and weapon identification in diverse video contexts (MDPI, 2023; Wiley, 2021).

**Evacuation Route Planning:** Dynamic evacuation modeling relies on graph algorithms. Implementations using Dijkstra's and A* effectively generate the shortest-safe routes in changing environments (ScienceDirect, 2020; 2024).

**RESEARCH GAP:** Existing work treats multi-hazard detection and evacuation routing as separate siloed problems. Moreover, there is an over-reliance on standard YOLO models that lack global image context. This project integrates CV-based multi-hazard detection with automatic rerouting, explicitly investigating the use of transformer architectures for higher detection accuracy in complex indoor environments.

***

### Slide 6: PROPOSED SYSTEM
**Overview:** A unified Python-based pipeline that processes surveillance video to automatically detect hazards and compute safe exit paths.

**Architecture / Workflow:**
1. **Input:** Video feed is ingested into the system.
2. **Parallel Processing:** Three checks occur simultaneously: Fire/Smoke Detection, Person/Weapon Detection, and Zone Rule Evaluation.
3. **Alert Classification:** The system classifies the event. Suspicious activity (e.g., restricted zone breach) generates an alert-only notification.
4. **Evacuation Trigger:** If a fire is detected, the exact location is passed to the routing engine.
5. **Dynamic Routing:** The floor plan graph blocks the affected node, and A*/Dijkstra algorithms compute the new safest route to display on the dashboard.

***

### Slide 7: DATASETS REFERRED FOR TRAINING

*   **Fire & Smoke Detection Datasets:** Aggregation of publicly available large-scale thermal anomaly and smoke datasets (e.g., [Fire and Smoke Detection Dataset from Kaggle](https://www.kaggle.com/datasets/hussainnasirkhan/fire-and-smoke-detection-dataset)) containing diverse indoor and outdoor fire scenarios.
*   **Weapon & Suspicious Activity Datasets:** Annotated surveillance footage and images specifically curated for weapon detection and anomalous human behavior in restricted zones (e.g., [Weapons Detection Dataset](https://www.kaggle.com/datasets/mralhasan/weapons-detection-dataset) and [Human Detection Dataset](https://www.kaggle.com/datasets/constantinwerner/human-detection-dataset)).
*   **Dataset Preprocessing:** Data is augmented (rotation, scaling, brightness adjustments) to improve robustness against varying lighting and angles typical of indoor CCTV footage.
*   **Annotation Formatting:** Datasets are formatted suitably for modern computer vision models (bounding boxes, classifications) to ensure high-accuracy training for both CNN and Transformer pipelines.

***

### Slide 8: MODEL IMPLEMENTATION & APPROACH

*   **Current Baseline:** Initially evaluating YOLO (You Only Look Once) variants (like YOLOv8n) due to their fast real-time inference and widespread baseline use.
*   **Transformer-Based Objective:** Our primary objective is to advance beyond standard YOLO versions by implementing **Vision Transformers (ViTs)** or hybrid transformer models (e.g., RT-DETR) for detection.
*   **Context & Justification:**
    *   **Global Context Awareness:** Transformers capture long-range dependencies across the entire image via self-attention mechanisms, improving accuracy in complex scenes where hazards might be partially occluded.
    *   **Reduced False Positives:** Better contextual understanding helps distinguish between actual fires and fire-like objects (e.g., bright lights), as well as between actual weapons and everyday objects.
    *   **State-of-the-Art Performance:** Transformer architectures are increasingly outperforming purely convolutional networks (CNNs) in complex visual understanding and robust feature extraction tasks.

***

### Slide 9: SOFTWARE & HARDWARE REQUIREMENTS

**Software Stack:**
*   **Language:** Python
*   **Backend Framework:** FastAPI, Uvicorn
*   **Frontend / UI:** Streamlit
*   **Computer Vision:** Vision Transformers (ViT) / Ultralytics (YOLOv8 baseline), OpenCV
*   **Graph Routing & Visualization:** NetworkX, Matplotlib

**Hardware Requirements:**
*   **Training:** Cloud GPU instances (Kaggle/Colab) are utilized for training the compute-intensive transformer models.
*   **Inference & Deployment:** Multi-core CPU with a minimum of 8GB RAM (16GB recommended); a dedicated GPU is preferred for real-time transformer inference.

***

### Slide 10: PROJECT TIMELINE & PROGRESS
*   **First Review (Current State):** Finalized project brief, literature review, system architecture, and completed dataset aggregation. Evaluated YOLOv8 baseline for Fire Detection. Implemented base mock floor plan routing using NetworkX and initial zone-rule logic.
*   **Second Review (Upcoming):** Transitioning detection modules to Transformer-based architectures. Full integration of the individual modules via the FastAPI backend. Tuning of the Suspicious Activity/Weapon detection rules.
*   **Final Review:** Completion of the Streamlit dashboard UI, end-to-end testing with demo videos, finalizing transformer vs. YOLO model comparison metrics, and documentation.

***

### Slide 11: CONCLUSION
In summary, this project addresses the critical gap of disconnected building safety systems by proposing a unified, CV-driven dashboard. We have established the core architecture, aggregated necessary datasets, and set up our foundational evacuation graph. While traditional models like YOLO offer a baseline, our core focus is leveraging Vision Transformers for enhanced context-awareness and accuracy. The next phase centers on implementing these transformer architectures and fully integrating them with our automated dynamic routing backend.

***

### Slide 12: REFERENCES
1. *[Early Fire and Smoke Detection Using Deep Learning: A Comprehensive Review of Models, Datasets, and Challenges](https://www.mdpi.com/2076-3417/15/18/10255)* (MDPI Applied Sciences, 2025)
2. *[An Improved Fire and Smoke Detection Method Based on YOLOv8n for Smart Factories](https://www.mdpi.com/1424-8220/24/15/4786)* (MDPI Sensors, 2024)
3. *[Indoor fire and smoke detection based on optimized YOLOv5](https://pmc.ncbi.nlm.nih.gov/articles/PMC12040180/)* (PMC, 2025)
4. *[Application of Deep Learning for Weapons Detection in Surveillance Videos](https://www.researchgate.net/publication/352095753_Application_of_Deep_Learning_for_Weapons_Detection_in_Surveillance_Videos)* (ResearchGate, 2021)
5. *[Weapon Detection Using YOLO V3 for Smart Surveillance System](https://onlinelibrary.wiley.com/doi/10.1155/2021/9975700)* (Wiley, Mathematical Problems in Engineering, 2021)
6. *[AI-Based Weapon Detection for Security Surveillance: Recent Research Advances 2016–2025](https://www.mdpi.com/2079-9292/14/23/4609)* (MDPI Electronics, 2025)
7. *[Deep Learning-Based Anomaly Detection in Video Surveillance: A Survey](https://pmc.ncbi.nlm.nih.gov/articles/PMC10255829/)* (MDPI Sensors, 2023)
8. *[A Comprehensive Review on Deep Learning-Based Methods for Video Anomaly Detection](https://www.sciencedirect.com/science/article/abs/pii/S0262885620302109)* (ScienceDirect)
9. *[EvacuSafe: A Real-Time Model for Building Evacuation Based on Dijkstra's Algorithm](https://www.sciencedirect.com/science/article/abs/pii/S2352710219324982)* (ScienceDirect, 2020)
10. *[A Dijkstra-Based Algorithm for Selecting the Shortest-Safe Evacuation Routes in Dynamic Environments](https://www.researchgate.net/publication/318145370_A_Dijkstra-Based_Algorithm_for_Selecting_the_Shortest-Safe_Evacuation_Routes_in_Dynamic_Environments_SSER)* (ResearchGate)
11. *[Escape Route Planning in Forest Fire Scenes Based on the Improved A* Algorithm](https://www.sciencedirect.com/science/article/pii/S1470160X24008124)* (ScienceDirect, 2024)

