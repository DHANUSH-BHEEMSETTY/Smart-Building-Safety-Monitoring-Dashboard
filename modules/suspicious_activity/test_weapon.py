import os
import cv2
import numpy as np
import detection

def run_test():
    print("--- Running Weapon Detection Test ---")
    
    # Create a blank test frame
    frame = np.ones((480, 640, 3), dtype=np.uint8) * 128  # gray frame

    # Try to load the weapon model
    weapon_model = detection.get_weapon_model()
    
    # Check if fine-tuned model is available
    if not detection._weapon_model_available:
        print("\nNote: Fine-tuned weapon model not available.")
        print("Weapon detection is correctly DISABLED to prevent false positives.")
        print("To enable, download the trained weights from Kaggle and place at:")
        print("  models/yolo11n_weapon_best.pt")
        print("\nDemonstrating with mock detection to verify alert pipeline...")
        
        # Override the detect_weapon function locally for the test
        original_detect_weapon = detection.detect_weapon
        def mock_detect_weapon(frame, conf_threshold=0.65):
            return [(150, 200, 350, 400, 0.92, 0, "gun")]
            
        detection.detect_weapon = mock_detect_weapon
    
    # Run the weapon detection (real or mock)
    boxes = detection.detect_weapon(frame)
    
    if len(boxes) > 0:
        print(f"\n[!] ALERT TRIGGERED: 'weapon_detected' [!]")
        print(f"Found {len(boxes)} weapon(s) in the frame.")
        for i, box in enumerate(boxes):
            x1, y1, x2, y2, conf, cls_id, class_name = box
            print(f"  Weapon {i+1} -> {class_name} | BBox: ({x1},{y1})-({x2},{y2}) | Confidence: {conf:.2f}")
    else:
        print("No weapons detected (model may be correctly filtering normal scene).")

if __name__ == "__main__":
    run_test()
