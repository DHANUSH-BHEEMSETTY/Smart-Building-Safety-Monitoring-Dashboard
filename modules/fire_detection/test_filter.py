import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.fire_detection.inference import FireAlertManager

def simulate_detections(scenario_name, frames_detections):
    print(f"\n=======================================================")
    print(f"🔬 SCENARIO: {scenario_name}")
    print(f"=======================================================")
    
    # Active production settings: 6-frame window, 3-frame threshold, 2.0% area threshold
    alert_manager = FireAlertManager(history_size=6, alert_threshold=3, area_threshold_pct=2.0)
    frame_shape = (1080, 1920) # 1080p frame
    
    for i, frame_det in enumerate(frames_detections):
        status, conf, area_pct = alert_manager.process_detections(frame_det, frame_shape)
        action = "🚨 DISPATCH TELEGRAM & EVAC" if status == "FULL_ALERT" else ("ℹ️ LOGGED ONLY (NO ALARM)" if status == "MINOR_LOW_SEVERITY" else "🟢 NORMAL (ZONE SECURED)")
        print(f"Frame {i+1:2d} | Status: {status:18s} | Conf: {conf:.2f} | Area: {area_pct:4.2f}% | Action: {action}")

def main():
    # Small flame: 0.5% screen area (e.g. cigarette lighter, matchstick, candle flame)
    # Area = 100x103 = 10,300 px (~0.50% of 1080x1920)
    small_flame = [{"conf": 0.85, "xyxy": [100, 100, 200, 203]}]
    
    # Large flame: 4.5% screen area (e.g. real growing corridor/room fire)
    large_flame = [{"conf": 0.92, "xyxy": [100, 100, 400, 412]}]
    
    # Scenario 1: Brief Lighter / Match Flick (lasts only 2 frames, small area)
    sc1 = []
    for i in range(8):
        if i in (1, 2):
            sc1.append(small_flame)
        else:
            sc1.append([])
    simulate_detections("Brief Lighter/Match Flicker (Transient < 3 frames, < 2.0% area)", sc1)
    
    # Scenario 2: Intermittent Reflections / Glare Glitches (1 frame every few frames)
    sc2 = []
    for i in range(8):
        if i in (0, 4):
            sc2.append(small_flame)
        else:
            sc2.append([])
    simulate_detections("Intermittent Optical Glare / Glitches (Never sustained)", sc2)

    # Scenario 3: Real Outbreak / Large Flame (Area >= 2.0%)
    sc3 = [large_flame] * 6
    simulate_detections("Real Flame Outbreak (Area >= 2.0% -> Instant Full Emergency)", sc3)
    
    # Scenario 4: Small Flame that Grows Sustained (Persists for 3+ consecutive frames)
    sc4 = [[]] + [small_flame] * 5
    simulate_detections("Small Flame that Becomes Sustained (Persists >= 3 frames -> Escalates to Full Alert)", sc4)

if __name__ == "__main__":
    main()
