from ultralytics import YOLO
import os

model = None

def get_model():
    global model
    if model is None:
        model = YOLO("yolov8n.pt")  # use pre-trained weights for general person detection
    return model

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

weapon_model = None

def get_weapon_model():
    global weapon_model
    if weapon_model is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        weights_path = os.path.join(base_dir, "runs", "weapon_det", "weights", "best.pt")
        
        if not os.path.exists(weights_path):
            print(f"Warning: Fine-tuned weapon model not found at {weights_path}. Using placeholder yolov8n.pt.")
            weapon_model = YOLO("yolov8n.pt")
        else:
            weapon_model = YOLO(weights_path)
    return weapon_model

def detect_weapon(frame, conf_threshold=0.5):
    """
    Takes an OpenCV frame, runs fine-tuned YOLOv8, and returns a list of bounding boxes for weapons.
    Each box is a tuple (x1, y1, x2, y2, confidence, class_id).
    """
    m = get_weapon_model()
    results = m(frame, verbose=False)
    
    weapon_boxes = []
    
    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0].item())
            cls_id = int(box.cls[0].item())
            
            # Assuming all classes in the fine-tuned dataset correspond to weapons (e.g. pistol, knife, etc.)
            if conf >= conf_threshold:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                weapon_boxes.append((x1, y1, x2, y2, conf, cls_id))
                
    return weapon_boxes
