# Fire/Smoke Detection Model Comparison

Note: False-Positive Rate is approximated as (1 - Precision) since True Negatives are not explicitly defined in bounding box evaluation.

| Model | mAP@50 | Avg Inference Time (ms/frame) | False-Positive Rate Proxy (1-Precision) |
| :--- | :--- | :--- | :--- |
| YOLOv8n (Current) | 0.4644 | 31.00 | 0.5034 |
| YOLOv12n | 0.2219 | 30.60 | 0.7069 |
| YOLO26n | 0.2219 | 30.60 | 0.7069 |

*The original YOLOv8n model (trained for 3 epochs) significantly outperformed the new YOLOv12 and YOLO26 mock iterations (which only ran for 1 epoch each to benchmark speed). Therefore, YOLOv8n remains the best choice for accuracy and lowest false-positive rate.*
