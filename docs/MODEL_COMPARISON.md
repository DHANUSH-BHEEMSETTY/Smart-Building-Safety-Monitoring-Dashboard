# Fire/Smoke Detection Model Comparison (Kaggle Training Results)

The following models were trained for 15 epochs on the Fire & Smoke dataset using Kaggle T4 GPUs:

| Model | mAP@50 | mAP@50-95 |
| :--- | :--- | :--- |
| **YOLOv8n** | 0.7089 | 0.4017 |
| **YOLOv11n** | 0.7073 | 0.3976 |
| **YOLO26n** | 0.6804 | 0.3813 |
| **RT-DETR-L** | 0.7059 | 0.3931 |

*Note: All models performed exceptionally well after 15 epochs. While YOLOv8n achieved a marginally higher mAP score, YOLOv11n provides a great balance of speed and modern architecture.*
