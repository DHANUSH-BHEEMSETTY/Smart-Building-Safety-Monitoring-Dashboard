import os
from detection import detect_person
from rules import check_rules, load_zone_config
import cv2
import numpy as np

def run_tests():
    config_path = os.path.join(os.path.dirname(__file__), "zone_config.json")
    zone_config = load_zone_config(config_path)
    
    # 1. Test check_rules manually
    print("--- Testing Rules Logic ---")
    
    # Simulate a person inside Zone A (polygon: 100,100 to 400,400)
    # Bottom center (feet_x, feet_y) inside 100-400
    person_box = (200, 150, 300, 350) 
    
    # Test during restricted hours (Zone A: 21:00 - 06:00)
    is_suspicious, reason = check_rules(person_box, "2026-08-13 22:30:00", zone_config)
    print(f"Test 1 (Inside Zone A at 22:30): Suspicious={is_suspicious} | Reason: {reason}")
    assert is_suspicious == True

    # Test outside restricted hours
    is_suspicious, reason = check_rules(person_box, "2026-08-13 14:00:00", zone_config)
    print(f"Test 2 (Inside Zone A at 14:00): Suspicious={is_suspicious} | Reason: {reason}")
    assert is_suspicious == False

    # Simulate a person outside Zone A and B
    person_box_out = (500, 500, 600, 600)
    is_suspicious, reason = check_rules(person_box_out, "2026-08-13 23:30:00", zone_config)
    print(f"Test 3 (Outside zones at 23:30): Suspicious={is_suspicious} | Reason: {reason}")
    assert is_suspicious == False

    # 2. Test detect_person (mocking an image)
    print("\n--- Testing Detection Model ---")
    # Create a blank white image
    mock_frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
    print("Running YOLOv8 on mock empty frame...")
    boxes = detect_person(mock_frame)
    print(f"Detected {len(boxes)} persons (expected 0 on blank frame).")
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    run_tests()
