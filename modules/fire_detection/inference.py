import os
import cv2
from ultralytics import YOLO

# Global config
MODEL_VERSION = "yolov8"  # Set to the best performing model (YOLOv8 outperformed others due to more epochs)

# Global model instance
model = None

def get_model():
    global model
    if model is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        
        if MODEL_VERSION == "yolov8":
            weights_path = os.path.join(base_dir, "runs", "fire_smoke_det", "weights", "best.pt")
        elif MODEL_VERSION == "yolov12":
            weights_path = os.path.join(base_dir, "runs_benchmark", "YOLOv12n_finetune", "weights", "best.pt")
        elif MODEL_VERSION == "yolo26":
            weights_path = os.path.join(base_dir, "runs_benchmark", "YOLO26n_finetune", "weights", "best.pt")
        else:
            raise ValueError(f"Unsupported MODEL_VERSION: {MODEL_VERSION}")
            
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Model weights not found at {weights_path}. Have you run the training or benchmark scripts?")
        model = YOLO(weights_path)
    return model

def detect_fire_raw(frame, conf_threshold=0.5):
    """
    Runs YOLO inference on a frame and returns raw detections above the confidence threshold.
    """
    m = get_model()
    results = m(frame, verbose=False)
    
    detections = []
    for r in results:
        for box in r.boxes:
            conf = box.conf[0].item()
            if conf >= conf_threshold:
                detections.append({
                    "conf": conf,
                    "xyxy": box.xyxy[0].cpu().numpy(),
                    "cls": int(box.cls[0].item())
                })
    return detections

from collections import deque

class FireAlertManager:
    def __init__(self, history_size=10, alert_threshold=8, area_threshold_pct=5.0):
        """
        history_size: Number of frames to track for persistence.
        alert_threshold: Minimum number of positive frames in history to trigger a sustained alert.
        area_threshold_pct: Minimum bounding box area percentage to trigger an immediate alert (large fire).
        """
        self.history = deque(maxlen=history_size)
        self.alert_threshold = alert_threshold
        self.area_threshold_pct = area_threshold_pct

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

def detect_fire(frame, conf_threshold=0.5):
    """
    Backwards compatible detect_fire function.
    Returns (fire_detected, highest_confidence).
    """
    detections = detect_fire_raw(frame, conf_threshold)
    fire_detected = len(detections) > 0
    highest_conf = max([d['conf'] for d in detections]) if fire_detected else 0.0
    return fire_detected, highest_conf

if __name__ == "__main__":
    import glob
    import random
    
    test_images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "fire_dataset", "fire_smoke", "test", "images"))
    
    if os.path.exists(test_images_dir):
        image_paths = glob.glob(os.path.join(test_images_dir, "*.jpg")) + glob.glob(os.path.join(test_images_dir, "*.png"))
        if image_paths:
            sample_paths = random.sample(image_paths, min(5, len(image_paths)))
            alert_manager = FireAlertManager()
            
            print(f"Testing advanced inference on {len(sample_paths)} sample images...")
            for img_path in sample_paths:
                frame = cv2.imread(img_path)
                if frame is None:
                    continue
                
                detections = detect_fire_raw(frame)
                status, conf, area_pct = alert_manager.process_detections(detections, frame.shape)
                
                print(f"[{os.path.basename(img_path)}] Status: {status} | Max Conf: {conf:.2f} | Area: {area_pct:.2f}%")
