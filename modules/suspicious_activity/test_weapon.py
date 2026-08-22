import os
import cv2
import numpy as np
import detection

def mock_yolo_result(frame, verbose=False):
    class MockBox:
        def __init__(self):
            import torch
            self.conf = torch.tensor([0.92])
            self.cls = torch.tensor([0]) # 0 for handgun/weapon in custom dataset
            self.xyxy = torch.tensor([[150, 200, 350, 400]])

    class MockResult:
        def __init__(self):
            self.boxes = [MockBox()]

    return [MockResult()]

def run_test():
    print("--- Running Weapon Detection Test ---")
    
    # Try to grab an image from the downloaded dataset
    import kagglehub
    try:
        dataset_path = kagglehub.dataset_download('raghavnanjappan/weapon-dataset-for-yolov5')
        import glob
        images = glob.glob(os.path.join(dataset_path, "**", "*.jpg"), recursive=True)
        if images:
            img_path = images[0]
            print(f"Using sample image from dataset: {os.path.basename(img_path)}")
            frame = cv2.imread(img_path)
        else:
            frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
    except Exception:
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    # Retrieve the model
    weapon_model = detection.get_weapon_model()
    
    # If the user hasn't fine-tuned the model yet, it defaults to yolov8n.pt. 
    # To demonstrate the alert logic without requiring a 1+ hour training session first, we mock it.
    if hasattr(weapon_model, "ckpt_path") and weapon_model.ckpt_path.endswith("yolov8n.pt"):
        print("Note: Fine-tuned weights not found yet. Using a mock YOLO detection to demonstrate the 'weapon_detected' alert pipeline.")
        
        # Override the detect_weapon function locally for the test
        original_detect_weapon = detection.detect_weapon
        def mock_detect_weapon(frame, conf_threshold=0.5):
            return [(150, 200, 350, 400, 0.92, 0)]
            
        detection.detect_weapon = mock_detect_weapon
    
    # Run the function we just added (or the mock if overridden)
    boxes = detection.detect_weapon(frame)
    
    if len(boxes) > 0:
        print(f"\n[!] ALERT TRIGGERED: 'weapon_detected' [!]")
        print(f"Found {len(boxes)} weapon(s) in the frame.")
        for i, box in enumerate(boxes):
            print(f"  Weapon {i+1} -> Bounding Box: {box[:4]}, Confidence: {box[4]:.2f}, Class ID: {box[5]}")
    else:
        print("No weapons detected.")

if __name__ == "__main__":
    run_test()
