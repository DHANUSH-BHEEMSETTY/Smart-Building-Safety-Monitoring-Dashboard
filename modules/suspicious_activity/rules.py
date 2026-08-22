import json
import cv2
import numpy as np
from datetime import datetime

def load_zone_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f).get("zones", [])

def is_point_in_polygon(point, polygon):
    """
    Checks if a (x, y) point is inside a polygon using OpenCV.
    polygon is a list of [x, y] coordinates.
    """
    pts = np.array(polygon, np.int32)
    pts = pts.reshape((-1, 1, 2))
    # pointPolygonTest returns +1 for inside, -1 for outside, 0 on an edge
    result = cv2.pointPolygonTest(pts, (float(point[0]), float(point[1])), False)
    return result >= 0

def is_time_restricted(current_time_str, start_time_str, end_time_str):
    """
    Checks if current_time (HH:MM) is between start_time and end_time.
    Handles cases where restricted time crosses midnight (e.g., 21:00 to 06:00).
    """
    fmt = "%H:%M"
    # Extract only HH:MM if a full timestamp was provided
    if " " in current_time_str:
        current_time_str = current_time_str.split(" ")[1][:5]
        
    curr = datetime.strptime(current_time_str, fmt).time()
    start = datetime.strptime(start_time_str, fmt).time()
    end = datetime.strptime(end_time_str, fmt).time()

    if start <= end:
        return start <= curr <= end
    else:
        # Crosses midnight
        return curr >= start or curr <= end

def check_rules(person_box, timestamp, zone_config):
    """
    Evaluates if a person is in a restricted zone during restricted hours.
    person_box: (x1, y1, x2, y2) or (x1, y1, x2, y2, conf)
    timestamp: "YYYY-MM-DD HH:MM:SS" or "HH:MM"
    zone_config: list of zone dictionaries loaded from JSON
    
    Returns: (is_suspicious: bool, reason: str)
    """
    # Calculate bottom-center of the bounding box (representing feet location)
    x1, y1, x2, y2 = person_box[:4]
    feet_x = (x1 + x2) / 2
    feet_y = y2
    feet_point = (feet_x, feet_y)

    for zone in zone_config:
        name = zone.get("name")
        polygon = zone.get("polygon")
        start_time = zone.get("restricted_start")
        end_time = zone.get("restricted_end")

        if is_point_in_polygon(feet_point, polygon):
            if is_time_restricted(timestamp, start_time, end_time):
                reason = f"Person detected in '{name}' during restricted hours ({start_time} - {end_time})"
                return True, reason
                
    return False, "Normal activity"
