import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
import cv2
import numpy as np
from datetime import datetime
import json

from modules.fire_detection.inference import detect_fire
from modules.suspicious_activity.detection import detect_person, detect_weapon
from modules.suspicious_activity.rules import check_rules, load_zone_config
from modules.evacuation_routing.floor_plan import create_floor_plan_graph, find_escape_route, plot_floor_plan
from modules.notifications.telegram_bot import notify_security

app = FastAPI()

# Load zone config
ZONE_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules", "suspicious_activity", "zone_config.json"))
zone_config = load_zone_config(ZONE_CONFIG_PATH)

# Initialize floor plan graph
floor_graph = create_floor_plan_graph()

@app.post("/analyze-frame")
async def analyze_frame(file: UploadFile = File(...), zone: str = Form("102")):
    # Read the image frame
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if frame is None:
        return JSONResponse(status_code=400, content={"error": "Invalid image file"})

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Detect Fire
    is_fire, fire_conf = detect_fire(frame)
    if is_fire:
        # It's a non-minor fire alert
        details = f"Location: {zone}\nTime: {current_time}\nConfidence: {fire_conf:.2f}"
        notify_security("fire", details)
        return {"tag": "fire", "confidence": fire_conf}

    # 2. Detect Weapon
    weapon_boxes = detect_weapon(frame)
    if weapon_boxes:
        details = f"Location: {zone}\nTime: {current_time}\nDetails: {len(weapon_boxes)} weapon(s) detected."
        notify_security("weapon_detected", details)
        return {"tag": "weapon_detected", "reason": f"{len(weapon_boxes)} weapon(s) detected"}

    # 3. Detect Person & Check Rules
    person_boxes = detect_person(frame)
    for box in person_boxes:
        is_suspicious, reason = check_rules(box, current_time, zone_config)
        if is_suspicious:
            details = f"Location: {zone}\nTime: {current_time}\nReason: {reason}"
            notify_security("suspicious_activity", details)
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
