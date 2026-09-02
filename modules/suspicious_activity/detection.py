from ultralytics import YOLO
import os

# ---------------------------------------------------------------------------
# Person detection — uses generic COCO pretrained model (class 0 = person)
# ---------------------------------------------------------------------------
_person_model = None

def get_model():
    global _person_model
    if _person_model is None:
        _person_model = YOLO("yolov8n.pt")  # COCO pretrained — class 0 is 'person'
    return _person_model

def detect_person(frame, conf_threshold=0.5):
    """
    Takes an OpenCV frame, runs YOLOv8, and returns a list of bounding boxes for persons.
    Each box is a tuple (x1, y1, x2, y2, confidence).
    """
    m = get_model()
    # Run inference
    results = m(frame, verbose=False)

    person_boxes = []

    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0].item())
            cls_id = int(box.cls[0].item())

            # class 0 in COCO dataset is 'person'
            if cls_id == 0 and conf >= conf_threshold:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                person_boxes.append((x1, y1, x2, y2, conf))

    return person_boxes


# ---------------------------------------------------------------------------
# Weapon detection — uses fine-tuned YOLOv11 model
# ---------------------------------------------------------------------------
_weapon_model = None
_weapon_model_available = False  # True only when fine-tuned weapon weights exist

# Class names for the YOLOv11 weapon model (nc=2)
WEAPON_CLASS_NAMES = ['gun', 'knife']

def get_weapon_model():
    global _weapon_model, _weapon_model_available
    if _weapon_model is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        # Priority 1: YOLOv11 fine-tuned weights (from Kaggle training)
        yolo11_path = os.path.join(base_dir, "models", "yolo11n_weapon_best.pt")

        # Priority 2: Legacy path (from local training runs)
        legacy_path = os.path.join(base_dir, "runs", "weapon_det", "weights", "best.pt")

        if os.path.exists(yolo11_path):
            print(f"[WeaponDetection] Loading YOLOv11 weapon model from {yolo11_path}")
            _weapon_model = YOLO(yolo11_path)
            _weapon_model_available = True
        elif os.path.exists(legacy_path):
            print(f"[WeaponDetection] YOLOv11 weights not found. Using legacy weights at {legacy_path}")
            _weapon_model = YOLO(legacy_path)
            _weapon_model_available = True
        else:
            print(
                f"[WeaponDetection] WARNING: No fine-tuned weapon model found.\n"
                f"  Expected YOLOv11: {yolo11_path}\n"
                f"  Fallback legacy:  {legacy_path}\n"
                f"  Weapon detection will be DISABLED to prevent false positives.\n"
                f"  See models/README.md for instructions on downloading trained weights."
            )
            _weapon_model_available = False
            # Load a dummy model so the variable is not None on next call,
            # but detect_weapon() will short-circuit before using it.
            _weapon_model = YOLO("yolov8n.pt")
    return _weapon_model


def detect_weapon(frame, conf_threshold=0.50):
    """
    Takes an OpenCV frame, runs the fine-tuned YOLOv11 weapon model, and returns
    a list of bounding boxes for weapons.
    
    Each box is a tuple (x1, y1, x2, y2, confidence, class_id, class_name).
    
    Confidence threshold raised to 0.65 (from 0.6) since the model was trained
    specifically on weapon data and higher thresholds reduce false positives.
    
    Returns an empty list when the fine-tuned weapon model is not available,
    to avoid false positives from the generic COCO model.
    """
    get_weapon_model()  # ensure model is loaded and flag is set

    # If no fine-tuned weapon model is available, skip detection entirely
    # to prevent the generic COCO model from flagging everyday objects as weapons.
    if not _weapon_model_available:
        return []

    results = _weapon_model(frame, verbose=False)

    weapon_boxes = []

    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0].item())
            cls_id = int(box.cls[0].item())

            # All classes in the fine-tuned dataset correspond to weapons
            if conf >= conf_threshold:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                # Get human-readable class name
                class_name = WEAPON_CLASS_NAMES[cls_id] if cls_id < len(WEAPON_CLASS_NAMES) else f"weapon_{cls_id}"
                weapon_boxes.append((x1, y1, x2, y2, conf, cls_id, class_name))

    return weapon_boxes
