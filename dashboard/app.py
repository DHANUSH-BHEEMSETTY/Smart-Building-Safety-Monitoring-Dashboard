import streamlit as st
import cv2
import requests
import numpy as np
import tempfile
import time
import queue
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode

st.set_page_config(page_title="Security Monitoring Dashboard", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .header-pill {
        background-color: #2e3b32;
        color: #4caf50;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        float: right;
        margin-top: 15px;
    }
    .card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #3d3d3d;
        color: #fafafa;
    }
    .alert-fire {
        background-color: #4d1c1c;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #732a2a;
    }
    .alert-fire-title {
        color: #ffcccc;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .alert-suspicious {
        background-color: #5e4100;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #8c6200;
    }
    .alert-suspicious-title {
        color: #ffe082;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .alert-weapon {
        background-color: #4d1c1c;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #732a2a;
    }
    .alert-weapon-title {
        color: #ffcccc;
        font-weight: bold;
        margin-bottom: 5px;
        /* Make weapon distinct from fire */
        font-style: italic; 
    }
    .alert-minor {
        background-color: #383a45;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #4f5263;
    }
    .alert-minor-title {
        color: #ced4da;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .alert-detail {
        font-size: 0.9em;
        color: #a3a8b8;
    }
    .pipeline-step {
        margin-bottom: 8px;
        font-size: 0.95em;
        color: #fafafa;
    }
    .caption-text {
        font-size: 0.8em;
        color: #a3a8b8;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# README Note
st.info("💡 Note: Both the backend (uvicorn) and this dashboard (streamlit run) must be running simultaneously in separate terminals for full functionality.")

# HEADER
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.title("Smart Building Safety Monitoring Dashboard")
with col_h2:
    st.markdown('<div class="header-pill">System running</div>', unsafe_allow_html=True)

# Mode Selector
st.markdown("### Input Source")
input_mode = st.radio("Select Input Mode", ["Upload test video", "Live webcam"], horizontal=True)

if input_mode == "Upload test video":
    uploaded_video = st.file_uploader("Upload a test video", type=["mp4", "avi", "mov"])
else:
    uploaded_video = None

# Session State Initialization
if 'pipeline_log' not in st.session_state:
    st.session_state.pipeline_log = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Backend URLs
BACKEND_URL = "http://127.0.0.1:8000"
ANALYZE_ENDPOINT = f"{BACKEND_URL}/analyze-frame"
ROUTE_ENDPOINT = f"{BACKEND_URL}/evacuation-route"
CAMERA_ZONE = "102"

# Layout
col1, col2 = st.columns([2, 1])

webrtc_ctx = None
frame_queue = None

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('### Video feed')
    
    if input_mode == "Live webcam":
        frame_queue = queue.Queue(maxsize=1)
        
        def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")
            try:
                frame_queue.put_nowait(img)
            except queue.Full:
                pass
            return frame
            
        webrtc_ctx = webrtc_streamer(
            key="live-webcam",
            mode=WebRtcMode.SENDRECV,
            video_frame_callback=video_frame_callback,
            async_processing=True,
        )
    else:
        stframe = st.empty()
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('### Processing pipeline')
    pipeline_header = st.empty()
    pipeline_placeholder = st.empty()

with col2:
    st.markdown('### Alerts')
    alerts_placeholder = st.empty()
    
    st.markdown('### Evacuation route')
    st.markdown('<div class="card">', unsafe_allow_html=True)
    route_image_placeholder = st.empty()
    st.markdown('<div class="caption-text">Floor plan updates automatically when a fire is confirmed</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="caption-text">Alerts are color-coded by severity and appear the moment each check completes.</div>', unsafe_allow_html=True)

# Helper functions
def render_pipeline(frame_num, logs):
    pipeline_header.markdown(f"**Processing pipeline — frame {frame_num}**")
    html = '<div class="card">'
    for log in logs:
        html += f'<div class="pipeline-step">{log}</div>'
    html += '<div class="caption-text">Live — updates automatically as each new frame is processed</div></div>'
    pipeline_placeholder.markdown(html, unsafe_allow_html=True)

def render_alerts(alerts):
    import textwrap
    html = '<div>'
    for alert in reversed(alerts):
        html += textwrap.dedent(alert)
    html += '</div>'
    alerts_placeholder.markdown(html, unsafe_allow_html=True)

def process_frame_logic(frame):
    fire_triggered = False
    _, buffer = cv2.imencode('.jpg', frame)
    
    current_logs = ["✅ Frame captured and preprocessed"]
    
    try:
        response = requests.post(ANALYZE_ENDPOINT, data={"zone": CAMERA_ZONE}, files={"file": ("frame.jpg", buffer.tobytes(), "image/jpeg")})
        
        if response.status_code == 200:
            result = response.json()
            tag = result.get("tag")
            
            if tag == "normal":
                current_logs.append("✅ Fire/smoke model checked — no detection")
                current_logs.append("✅ Person detected — checking zone and time rules")
                current_logs.append("✅ Weapon model checked — no detection")
                
            elif tag == "suspicious":
                reason = result.get("reason", "Unknown")
                current_logs.append("✅ Fire/smoke model checked — no detection")
                current_logs.append("⚠️ Zone A after hours — rule triggered")
                current_logs.append("🔵 Security notified via message alert")
                
                alert_html = f"""
                <div class="alert-suspicious">
                    <div class="alert-suspicious-title">Suspicious activity — {CAMERA_ZONE}</div>
                    <div class="alert-detail">{reason} · alert only · security notified</div>
                </div>
                """
                st.session_state.alerts.append(alert_html)
                
            elif tag == "weapon_detected":
                reason = result.get("reason", "Unknown")
                current_logs.append("✅ Fire/smoke model checked — no detection")
                current_logs.append("⚠️ Weapon detected — rule triggered")
                current_logs.append("🔵 Security notified via message alert")
                
                alert_html = f"""
                <div class="alert-weapon">
                    <div class="alert-weapon-title">Weapon detected — {CAMERA_ZONE}</div>
                    <div class="alert-detail">{reason} · high confidence · security notified</div>
                </div>
                """
                st.session_state.alerts.append(alert_html)
                
            elif tag == "fire":
                current_logs.append("⚠️ Fire/smoke model checked — FIRE DETECTED")
                current_logs.append("🔵 Security notified via message alert")
                
                alert_html = f"""
                <div class="alert-fire">
                    <div class="alert-fire-title">Fire — room {CAMERA_ZONE}</div>
                    <div class="alert-detail">Confirmed after 9s sustained · route rerouted · security notified</div>
                </div>
                """
                st.session_state.alerts.append(alert_html)
                
                route_resp = requests.post(ROUTE_ENDPOINT, data={"fire_origin_room": CAMERA_ZONE})
                if route_resp.status_code == 200:
                    route_image_placeholder.image(route_resp.content, caption="Recommended Evacuation Route", use_container_width=True)
                    current_logs.append("🔵 Evacuation route generated")
                else:
                    st.error("Failed to fetch evacuation route.")
                    
                fire_triggered = True
                
            elif tag == "minor_fire":
                current_logs.append("✅ Fire/smoke model checked — minor flame")
                
                alert_html = f"""
                <div class="alert-minor">
                    <div class="alert-minor-title">Minor flame — {CAMERA_ZONE}</div>
                    <div class="alert-detail">Brief, small size · logged only · no alert sent</div>
                </div>
                """
                st.session_state.alerts.append(alert_html)
            
            for log in current_logs:
                st.session_state.pipeline_log.append(log)
            
            if len(st.session_state.pipeline_log) > 6:
                st.session_state.pipeline_log = st.session_state.pipeline_log[-6:]
                
    except Exception as e:
        st.session_state.pipeline_log.append(f"⚠️ Backend connection error: {e}")
        if len(st.session_state.pipeline_log) > 6:
            st.session_state.pipeline_log = st.session_state.pipeline_log[-6:]
            
    return fire_triggered

# Initial render
render_pipeline(0, st.session_state.pipeline_log)
render_alerts(st.session_state.alerts)

# --- Upload Mode Logic ---
if input_mode == "Upload test video" and uploaded_video is not None:
    if st.button("Start processing"):
        # Save uploaded file to a temporary file
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_video.read())
        video_path = tfile.name
        
        # Backend health check
        try:
            requests.get(BACKEND_URL, timeout=2)
        except requests.exceptions.RequestException:
            st.error("Backend not running. Start it first with: `uvicorn backend.main:app --reload --port 8000`")
            st.stop()
            
        cap = cv2.VideoCapture(video_path)
        fire_triggered = False
        
        while cap.isOpened() and not fire_triggered:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            stframe.image(frame, channels="BGR", use_container_width=True)
            
            if frame_num % 5 == 0:
                fire_triggered = process_frame_logic(frame)
            
            render_pipeline(frame_num, st.session_state.pipeline_log)
            if frame_num % 5 == 0:
                render_alerts(st.session_state.alerts)
                
            time.sleep(0.15) 
    
        cap.release()
        if not fire_triggered:
            st.info("Video processing complete.")

# --- Live Webcam Logic ---
if input_mode == "Live webcam" and webrtc_ctx is not None and webrtc_ctx.state.playing:
    # Backend health check
    try:
        requests.get(BACKEND_URL, timeout=2)
    except requests.exceptions.RequestException:
        st.error("Backend not running. Start it first with: `uvicorn backend.main:app --reload --port 8000`")
        st.stop()
        
    fire_triggered = False
    frame_num = 0
    
    while not fire_triggered:
        try:
            frame = frame_queue.get(timeout=1.0)
        except queue.Empty:
            if not webrtc_ctx.state.playing:
                break
            continue
            
        frame_num += 1
        
        # Process every 5th frame to avoid overwhelming the backend
        if frame_num % 5 == 0:
            fire_triggered = process_frame_logic(frame)
            
        render_pipeline(frame_num, st.session_state.pipeline_log)
        
        if frame_num % 5 == 0:
            render_alerts(st.session_state.alerts)
            
        # We don't sleep here since the frame_queue regulates the loop speed based on webcam FPS,
        # but a tiny sleep prevents CPU hogging if frames arrive too fast.
        time.sleep(0.01)
        
    if fire_triggered:
        st.info("Evacuation initiated. Webcam processing paused.")
