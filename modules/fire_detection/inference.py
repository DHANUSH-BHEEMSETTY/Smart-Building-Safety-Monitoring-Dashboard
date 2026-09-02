import os
import cv2
from ultralytics import YOLO
from collections import deque

# ---------------------------------------------------------------------------
# Model loading — YOLOv11 trained weights (preferred), fallback to YOLOv8
# ---------------------------------------------------------------------------
model = None

def get_model():
    global model
    if model is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        # Priority 1: YOLOv11 fine-tuned weights (from Kaggle training)
        yolo11_path = os.path.join(base_dir, "models", "yolo11n_fire_smoke_best.pt")

        # Priority 2: Legacy YOLOv8 weights (local training)
        yolov8_path = os.path.join(base_dir, "runs", "fire_smoke_det", "weights", "best.pt")

        if os.path.exists(yolo11_path):
            print(f"[FireDetection] Loading YOLOv11 fire/smoke model from {yolo11_path}")
            model = YOLO(yolo11_path)
        elif os.path.exists(yolov8_path):
            print(f"[FireDetection] YOLOv11 weights not found. Falling back to YOLOv8 weights at {yolov8_path}")
            model = YOLO(yolov8_path)
        else:
            raise FileNotFoundError(
                f"No fire/smoke model weights found.\n"
                f"  Expected YOLOv11: {yolo11_path}\n"
                f"  Fallback YOLOv8:  {yolov8_path}\n"
                f"Please ensure trained weights are located in the models/ directory."
            )
    return model


# ---------------------------------------------------------------------------
# Raw detection — returns all detections above the confidence threshold
# ---------------------------------------------------------------------------
def detect_fire_raw(frame, conf_threshold=0.35):
    """
    Runs YOLO inference on a frame and returns raw detections above the confidence threshold.
    Default threshold: 0.35 for robust, real-time fire and smoke localization.
    """
    m = get_model()
    results = m(frame, verbose=False)

    detections = []
    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0].item())
            if conf >= conf_threshold:
                detections.append({
                    "conf": conf,
                    "xyxy": box.xyxy[0].cpu().numpy(),
                    "cls": int(box.cls[0].item()),
                    "name": m.names.get(int(box.cls[0].item()), "hazard")
                })
    return detections


# ---------------------------------------------------------------------------
# FireAlertManager — Multi-frame temporal filtering to prevent false alerts
# ---------------------------------------------------------------------------
class FireAlertManager:
    def __init__(self, history_size=6, alert_threshold=3, area_threshold_pct=2.0):
        """
        Temporal filtering to distinguish real fires from transient single-frame glitches.
        
        history_size: Sliding window size (6 sampled frames ~ 1 sec of video).
        alert_threshold: 3 positive detections within window triggers FULL_ALERT.
        area_threshold_pct: Flame/smoke area >= 2.0% triggers immediate FULL_ALERT.
        """
        self.history = deque(maxlen=history_size)
        self.alert_threshold = alert_threshold
        self.area_threshold_pct = area_threshold_pct

    def reset(self):
        """Resets detection history (useful when starting a new video or session)."""
        self.history.clear()

    def process_detections(self, detections, frame_shape):
        """
        Process raw detections and apply filtering logic.
        Returns: (status, highest_conf, max_area_pct)
        status can be "NORMAL", "MINOR_LOW_SEVERITY", or "FULL_ALERT".
        """
        frame_area = frame_shape[0] * frame_shape[1]
        highest_conf = 0.0
        max_area_pct = 0.0

        for det in detections:
            conf = det['conf']
            if conf > highest_conf:
                highest_conf = conf

            x1, y1, x2, y2 = det['xyxy']
            area = (x2 - x1) * (y2 - y1)
            area_pct = (area / frame_area) * 100
            if area_pct > max_area_pct:
                max_area_pct = area_pct

        is_detected = len(detections) > 0
        self.history.append(is_detected)

        sustained = sum(self.history) >= self.alert_threshold
        large = max_area_pct >= self.area_threshold_pct

        status = "NORMAL"
        if is_detected:
            if sustained or large:
                status = "FULL_ALERT"
            else:
                status = "MINOR_LOW_SEVERITY"

        return status, highest_conf, max_area_pct


# ---------------------------------------------------------------------------
# Global alert manager instance — shared across frames for temporal filtering
# ---------------------------------------------------------------------------
_global_alert_manager = FireAlertManager(history_size=6, alert_threshold=3, area_threshold_pct=2.0)


def reset_fire_alert_history():
    """Resets the global persistence filter state."""
    _global_alert_manager.reset()


def detect_fire(frame, conf_threshold=0.35):
    """
    Main fire detection entry point with temporal filtering.
    
    Returns (status, highest_confidence) where status is one of:
      - "NORMAL" — no fire detected (or transient noise filtered out)
      - "MINOR_LOW_SEVERITY" — fire/smoke detected but building persistence history
      - "FULL_ALERT" — sustained fire (>=3 detections) or large hazard (>=2% area) confirmed
    """
    detections = detect_fire_raw(frame, conf_threshold)
    status, highest_conf, _ = _global_alert_manager.process_detections(detections, frame.shape)
    return status, highest_conf


# ---------------------------------------------------------------------------
# Standalone test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import numpy as np
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    status, conf = detect_fire(dummy_frame)
    print(f"Test on blank frame: Status={status}, Conf={conf:.2f}")
