import numpy as np
from inference import FireAlertManager

def simulate_detections(scenario_name, frames_detections):
    print(f"\n--- Running Scenario: {scenario_name} ---")
    alert_manager = FireAlertManager(history_size=10, alert_threshold=8, area_threshold_pct=5.0)
    
    frame_shape = (1080, 1920) # 1080p frame
    
    for i, frame_det in enumerate(frames_detections):
        status, conf, area_pct = alert_manager.process_detections(frame_det, frame_shape)
        print(f"Frame {i+1:2d} | Status: {status:20s} | Max Conf: {conf:.2f} | Max Area: {area_pct:5.2f}%")

def main():
    # Scenario 1: Small brief flame (e.g. ~1% area, lasts 3 frames)
    # A small flame [x1, y1, x2, y2] area = 1% of 1080x1920 = ~20,736 pixels (e.g. 100x207)
    small_flame = [{"conf": 0.85, "xyxy": [100, 100, 200, 307]}] # Area = 100 * 207 = 20700 (1.00%)
    
    scenario_1 = []
    for i in range(10):
        if 2 <= i <= 4:
            scenario_1.append(small_flame)
        else:
            scenario_1.append([]) # No detections
            
    simulate_detections("Small Brief Flame (Low Severity)", scenario_1)
    
    # Scenario 2: Large sustained flame (e.g. ~10% area, lasts all frames)
    # A large flame area = 10% of 1080x1920 = ~207,360 pixels (e.g. 400x518)
    large_flame = [{"conf": 0.95, "xyxy": [100, 100, 500, 618]}] # Area = 400 * 518 = 207200 (9.99%)
    
    scenario_2 = []
    for i in range(10):
        scenario_2.append(large_flame)
        
    simulate_detections("Large Sustained Flame (Full Alert)", scenario_2)

    # Scenario 3: Small but sustained flame
    scenario_3 = []
    for i in range(10):
        scenario_3.append(small_flame)
    simulate_detections("Small Sustained Flame (Full Alert after 8 frames)", scenario_3)

if __name__ == "__main__":
    main()
