import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
import cv2
import numpy as np
from datetime import datetime
import json

from modules.fire_detection.inference import detect_fire, reset_fire_alert_history
from modules.suspicious_activity.detection import detect_person, detect_weapon
from modules.suspicious_activity.rules import check_rules, load_zone_config
from modules.evacuation_routing.floor_plan import create_floor_plan_graph, find_escape_route, plot_floor_plan
from modules.notifications.telegram_notifier import send_telegram_alert, reset_rate_limits

app = FastAPI()

# Load zone config
ZONE_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules", "suspicious_activity", "zone_config.json"))
zone_config = load_zone_config(ZONE_CONFIG_PATH)

# Initialize floor plan graph
floor_graph = create_floor_plan_graph()

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Smart Building Safety Monitoring Dashboard Backend is running.",
        "docs": "/docs",
        "endpoints": {
            "analyze_frame": "/analyze-frame (POST)",
            "evacuation_route": "/evacuation-route (POST)",
            "docs": "/docs (GET)"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/reset")
async def reset_state():
    reset_fire_alert_history()
    reset_rate_limits()
    return {"status": "reset_complete"}


@app.post("/analyze-frame")
async def analyze_frame(file: UploadFile = File(...), zone: str = Form("102")):
    # Read the image frame
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return JSONResponse(status_code=400, content={"error": "Invalid image file"})

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Detect Fire/Smoke (with temporal filtering via FireAlertManager)
    #    detect_fire() returns (status, confidence) where status is:
    #    - "NORMAL" — no hazard or transient false positive
    #    - "MINOR_LOW_SEVERITY" — logged only, zero Telegram alerts dispatched
    #    - "FULL_ALERT" — sustained/large fire confirmed (dispatches Telegram + dynamic route)
    fire_status, fire_conf = detect_fire(frame)
    
    if fire_status == "FULL_ALERT":
        send_telegram_alert(alert_type="fire", location=zone, confidence=fire_conf)
        return {"tag": "fire", "confidence": fire_conf}
    
    if fire_status == "MINOR_LOW_SEVERITY":
        # Logged only, zero Telegram alerts dispatched
        return {"tag": "minor_fire", "confidence": fire_conf}

    # 2. Detect Weapon (using fine-tuned YOLOv11 model — gun and knife only)
    weapon_boxes = detect_weapon(frame)
    if weapon_boxes:
        weapon_descriptions = [f"{wb[6]} ({wb[4]:.2f})" for wb in weapon_boxes]
        details = f"{len(weapon_boxes)} weapon(s) identified: {', '.join(weapon_descriptions)}"
        send_telegram_alert(alert_type="weapon_detected", location=zone, details=details)
        return {
            "tag": "weapon_detected",
            "reason": details
        }

    # 3. Detect Person & Check Rules
    person_boxes = detect_person(frame)
    for box in person_boxes:
        is_suspicious, reason = check_rules(box, current_time, zone_config)
        if is_suspicious:
            send_telegram_alert(alert_type="suspicious_activity", location=zone, details=reason)
            return {"tag": "suspicious", "reason": reason}

    return {"tag": "normal"}

@app.post("/evacuation-route")
async def evacuation_route(fire_origin_room: str = Form(...)):
    # Find the escape route from the fire origin
    path = find_escape_route(floor_graph, fire_origin_room=fire_origin_room, blocked_rooms=[])
    
    if not path:
        return JSONResponse(status_code=404, content={"error": "No safe route found"})
        
    filename = f"route_{fire_origin_room}.png"
    plot_path = plot_floor_plan(floor_graph, fire_origin_room=fire_origin_room, path=path, filename=filename)
    
    return FileResponse(plot_path)
