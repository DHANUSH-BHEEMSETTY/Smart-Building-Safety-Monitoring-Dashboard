import streamlit as st
import cv2
import requests
import numpy as np
import tempfile
import time
import queue
import av
import html
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, WebRtcMode

st.set_page_config(
    page_title="SmartBuildAI — Intelligent Safety & Evacuation Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------------------------
# High-Tech SOC Command Center Aesthetics
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Body & Canvas Theme */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #06090F !important;
        color: #F1F5F9 !important;
    }

    /* Ambient Subtle Glow Mesh */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; height: 350px;
        background: radial-gradient(circle at 50% -30%, rgba(14, 165, 233, 0.12), rgba(99, 102, 241, 0.04) 50%, transparent 80%);
        pointer-events: none;
        z-index: 0;
    }

    /* Main Command Header */
    .smartbuild-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 24px;
        background: rgba(13, 19, 33, 0.85);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.7);
    }
    .brand-group {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .brand-logo {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #0284C7 0%, #06B6D4 50%, #3B82F6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.45);
    }
    .brand-text h1 {
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em;
        margin: 0 !important;
        background: linear-gradient(135deg, #FFFFFF 30%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .brand-subtitle {
        font-size: 0.8rem;
        color: #64748B;
        font-weight: 500;
        margin-top: 2px;
    }
    .header-telemetry {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 4px;
    }
    .system-active-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 5px 14px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 30px;
        color: #34D399;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        font-family: 'JetBrains Mono', monospace;
    }
    .system-clock {
        font-size: 0.8rem;
        color: #94A3B8;
        font-family: 'JetBrains Mono', monospace;
    }
    .pulse-dot-green {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
        animation: pulse-green 2s infinite ease-in-out;
    }
    @keyframes pulse-green {
        0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 10px #10B981; }
        50% { opacity: 0.3; transform: scale(0.85); box-shadow: 0 0 2px #10B981; }
    }

    /* Section Headers */
    .section-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94A3B8;
        font-weight: 800;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-sub {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 12px;
    }

    /* Glass Panels */
    .glass-panel {
        background: rgba(13, 19, 33, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 12px 35px -10px rgba(0, 0, 0, 0.6);
    }

    /* Video Overlay Status */
    .feed-container {
        position: relative;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: #000;
    }
    .feed-status-bar {
        padding: 10px 16px;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(12px);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.85rem;
        font-weight: 700;
    }
    .feed-status-normal { color: #34D399; }
    .feed-status-hazard { color: #F87171; animation: pulse-crit 1.5s infinite; }
    @keyframes pulse-crit {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    /* Secondary Camera Feeds Grid */
    .camera-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 18px;
    }
    .cam-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 8px;
        position: relative;
    }
    .cam-thumbnail {
        height: 95px;
        background: linear-gradient(135deg, #1E293B, #0F172A);
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #64748B;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
    }
    .cam-label {
        font-size: 0.75rem;
        font-weight: 700;
        color: #E2E8F0;
        margin-top: 6px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .cam-live-badge {
        font-size: 0.65rem;
        color: #10B981;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Alert Cards */
    .alert-box-fire {
        background: linear-gradient(135deg, rgba(127, 29, 29, 0.45) 0%, rgba(69, 10, 10, 0.75) 100%);
        border: 1px solid #EF4444;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.3);
        animation: fire-pulse 2s infinite ease-in-out;
    }
    @keyframes fire-pulse {
        0%, 100% { border-color: rgba(239, 68, 68, 0.9); }
        50% { border-color: rgba(239, 68, 68, 0.35); }
    }
    .alert-box-weapon {
        background: linear-gradient(135deg, rgba(120, 53, 15, 0.45) 0%, rgba(67, 20, 7, 0.7) 100%);
        border: 1px solid #F59E0B;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.25);
    }
    .alert-box-suspicious {
        background: linear-gradient(135deg, rgba(78, 56, 12, 0.4) 0%, rgba(35, 25, 5, 0.6) 100%);
        border: 1px solid #D97706;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .alert-box-minor {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .alert-head-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .alert-title-text {
        font-size: 0.95rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .ack-badge {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #F8FAFC;
    }

    /* Primary Launch Button */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(56, 189, 248, 0.5) !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        padding: 14px 28px !important;
        letter-spacing: 0.03em;
        box-shadow: 0 4px 20px rgba(2, 132, 199, 0.4) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(2, 132, 199, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# TOP HEADER: SmartBuildAI Command Center
# ---------------------------------------------------------------------------
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.markdown(f"""
<div class="smartbuild-header">
    <div class="brand-group">
        <div class="brand-logo">⚡</div>
        <div class="brand-text">
            <h1>SmartBuildAI Command Center</h1>
            <div class="brand-subtitle">AI-Powered Multi-Hazard Surveillance & Dynamic Evacuation Management</div>
        </div>
    </div>
    <div class="header-telemetry">
        <div class="system-active-pill">
            <span class="pulse-dot-green"></span>
            <span>SYSTEM ACTIVE • ALL ZONES</span>
        </div>
        <div class="system-clock">{now_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# INGESTION CONTROLS BAR
# ---------------------------------------------------------------------------
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1.8, 1])

with col_ctrl1:
    st.markdown('<div class="section-title">Select Ingestion Stream</div>', unsafe_allow_html=True)
    input_mode = st.radio("Stream Selection", ["Upload Video File", "Live Stream"], horizontal=True, label_visibility="collapsed")

with col_ctrl2:
    st.markdown('<div class="section-title">Ingest Security Footage</div>', unsafe_allow_html=True)
    if input_mode == "Upload Video File":
        uploaded_video = st.file_uploader("Upload video footage", type=["mp4", "avi", "mov"], label_visibility="collapsed")
    else:
        uploaded_video = None
        st.caption("Live Camera Stream selected — click START in the webcam panel below.")

with col_ctrl3:
    st.markdown('<div class="section-title">Stream Management</div>', unsafe_allow_html=True)
    selected_cam = st.selectbox("Active Camera", ["Camera 1 • Zone 102 (Corridor A)", "Camera 2 • Lobby 1", "Camera 3 • Perimeter North"], label_visibility="collapsed")

# Backend URLs
BACKEND_URL = "http://127.0.0.1:8000"
ANALYZE_ENDPOINT = f"{BACKEND_URL}/analyze-frame"
ROUTE_ENDPOINT = f"{BACKEND_URL}/evacuation-route"
CAMERA_ZONE = "102"

# Session State
if 'pipeline_log' not in st.session_state:
    st.session_state.pipeline_log = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# ---------------------------------------------------------------------------
# MAIN WORKSPACE GRID
# ---------------------------------------------------------------------------
col_left, col_right = st.columns([1.25, 1])

webrtc_ctx = None
frame_queue = None

with col_left:
    st.markdown('<div class="section-title">Real-Time Surveillance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Zone 102 (Corridor A)</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feed-container">', unsafe_allow_html=True)
    if input_mode == "Live Stream":
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
        
    feed_status_placeholder = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Alert Feed Panel
    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Threat & Response Alert Feed</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 0.8rem; color: #64748B; margin-bottom: 12px;">Real-time feed for high-priority active incidents.</div>', unsafe_allow_html=True)
    alerts_placeholder = st.empty()

with col_right:
    # Secondary CCTV Grid
    st.markdown('<div class="section-title">Multi-Camera Feed Matrix</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="camera-grid">
        <div class="cam-card">
            <div class="cam-thumbnail">📹 Lobby 1 [CAM-02]</div>
            <div class="cam-label"><span>Lobby 1</span> <span class="cam-live-badge">● LIVE</span></div>
        </div>
        <div class="cam-card">
            <div class="cam-thumbnail">📹 Perimeter [CAM-03]</div>
            <div class="cam-label"><span>Perimeter North</span> <span class="cam-live-badge">● LIVE</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Evacuation Route Section
    st.markdown('<div class="section-title">Evacuation Routing</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    route_image_placeholder = st.empty()
    st.markdown("""
    <div style="font-size: 0.78rem; color: #64748B; margin-top: 10px;">
        💡 <em>Dynamic graph automatically isolates fire origin room and computes the shortest obstacle-free escape path to Exit 3.</em>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# RENDERING HELPERS
# ---------------------------------------------------------------------------
def render_feed_status(status="NORMAL"):
    if status == "FULL_ALERT":
        html_s = """
        <div class="feed-status-bar">
            <span class="feed-status-hazard">🚨 FIRE ORIGIN DETECTED — Smoke & Thermal Persistence Validated</span>
            <span class="system-active-pill" style="border-color: #EF4444; color: #F87171; background: rgba(239, 68, 68, 0.15);">CRITICAL ALERT</span>
        </div>
        """
    else:
        html_s = """
        <div class="feed-status-bar">
            <span class="feed-status-normal">🟢 NORMAL MONITORING — Zone 102 Secured</span>
            <span class="system-active-pill">SURVEILLANCE ACTIVE</span>
        </div>
        """
    feed_status_placeholder.markdown(html_s, unsafe_allow_html=True)

def render_alerts(alerts):
    if not alerts:
        alerts_placeholder.markdown("""
        <div style="padding: 22px; text-align: center; color: #64748B; font-size: 0.88rem; background: rgba(15, 23, 42, 0.4); border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.08);">
            🟢 All monitoring zones clear • No active security incidents
        </div>
        """, unsafe_allow_html=True)
        return
        
    html_out = '<div>'
    for alert in reversed(alerts):
        html_out += alert
    html_out += '</div>'
    alerts_placeholder.markdown(html_out, unsafe_allow_html=True)

# Initial Renders
render_feed_status("NORMAL")
render_alerts(st.session_state.alerts)

# ---------------------------------------------------------------------------
# CORE FRAME PROCESSING PIPELINE
# ---------------------------------------------------------------------------
def process_frame_logic(frame, frame_num):
    fire_triggered = False
    _, buffer = cv2.imencode('.jpg', frame)
    current_time = time.strftime("%H:%M:%S")
    
    try:
        response = requests.post(ANALYZE_ENDPOINT, data={"zone": CAMERA_ZONE}, files={"file": ("frame.jpg", buffer.tobytes(), "image/jpeg")})
        
        if response.status_code == 200:
            result = response.json()
            tag = result.get("tag")
            conf = result.get("confidence", 0.0)
            
            if tag == "fire":
                render_feed_status("FULL_ALERT")
                
                alert_html = f"""
                <div class="alert-box-fire">
                    <div class="alert-head-row">
                        <div class="alert-title-text" style="color: #FCA5A5;">⚠️ CRITICAL FIRE HAZARD — Zone {CAMERA_ZONE}</div>
                        <span class="ack-badge">Acknowledge</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5;">
                        <strong>Location:</strong> Room/Corridor {CAMERA_ZONE} &nbsp;|&nbsp; <strong>Time:</strong> {current_time}<br>
                        <strong>Threat:</strong> Smoke/Thermal Confirmed ({conf:.2f}) &nbsp;|&nbsp; <strong>Security Dispatch:</strong> Instant & Deployed
                    </div>
                </div>
                """
                st.session_state.alerts.append(alert_html)
                
                route_resp = requests.post(ROUTE_ENDPOINT, data={"fire_origin_room": CAMERA_ZONE})
                if route_resp.status_code == 200:
                    route_image_placeholder.image(route_resp.content, caption="Recommended Safe Evacuation Route", use_container_width=True)
                else:
                    st.error("Failed to compute evacuation route.")
                    
                fire_triggered = True
                
            elif tag == "weapon_detected":
                reason = result.get("reason", "Weapon identified")
                
                alert_html = f"""
                <div class="alert-box-weapon">
                    <div class="alert-head-row">
                        <div class="alert-title-text" style="color: #FDE68A;">🚨 LETHAL THREAT: WEAPON DETECTED — Zone {CAMERA_ZONE}</div>
                        <span class="ack-badge">Acknowledge</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5;">
                        <strong>Location:</strong> Zone {CAMERA_ZONE} &nbsp;|&nbsp; <strong>Time:</strong> {current_time}<br>
                        <strong>Details:</strong> {html.escape(reason)} &nbsp;|&nbsp; <strong>Action:</strong> Priority Security Dispatch
                    </div>
                </div>
                """
                st.session_state.alerts.append(alert_html)
                
            elif tag == "suspicious":
                reason = result.get("reason", "Zone infraction")
                
                alert_html = f"""
                <div class="alert-box-suspicious">
                    <div class="alert-head-row">
                        <div class="alert-title-text" style="color: #FEF08A;">⚠️ Suspicious Activity — Zone {CAMERA_ZONE}</div>
                        <span class="ack-badge">Acknowledge</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5;">
                        <strong>Location:</strong> Zone {CAMERA_ZONE} &nbsp;|&nbsp; <strong>Time:</strong> {current_time}<br>
                        <strong>Infraction:</strong> {html.escape(reason)} &nbsp;|&nbsp; <strong>Action:</strong> Security Verification
                    </div>
                </div>
                """
                st.session_state.alerts.append(alert_html)
                
            elif tag == "minor_fire":
                alert_html = f"""
                <div class="alert-box-minor">
                    <div class="alert-head-row">
                        <div class="alert-title-text" style="color: #CBD5E1;">ℹ️ Minor Flame Trace — Zone {CAMERA_ZONE}</div>
                        <span class="ack-badge">Logged</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #94A3B8;">
                        Brief flame trace ({conf:.2f}) · Logged only · Awaiting persistence confirmation
                    </div>
                </div>
                """
                st.session_state.alerts.append(alert_html)
                
            else:
                render_feed_status("NORMAL")
                
    except Exception as e:
        st.warning(f"Backend connection note: {e}")
        
    return fire_triggered

# ---------------------------------------------------------------------------
# VIDEO UPLOAD STREAM PROCESSING
# ---------------------------------------------------------------------------
if input_mode == "Upload Video File" and uploaded_video is not None:
    if st.button("▶ Start AI Surveillance Pipeline"):
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        video_path = tfile.name
        
        # Reset backend state
        try:
            requests.get(BACKEND_URL, timeout=2)
            requests.post(f"{BACKEND_URL}/reset", timeout=2)
        except Exception:
            st.error("Backend offline. Launch it with: `uvicorn backend.main:app --reload --port 8000`")
            st.stop()
            
        st.session_state.alerts = []
        st.session_state.pipeline_log = []
        
        cap = cv2.VideoCapture(video_path)
        fire_triggered = False
        
        while cap.isOpened() and not fire_triggered:
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            stframe.image(frame, channels="BGR", use_container_width=True)
            
            if frame_num % 5 == 0:
                fire_triggered = process_frame_logic(frame, frame_num)
                render_alerts(st.session_state.alerts)
                
            time.sleep(0.12)
            
        cap.release()
        if not fire_triggered:
            st.info("Surveillance video playback complete. No sustained emergency detected.")

# ---------------------------------------------------------------------------
# LIVE STREAM PROCESSING
# ---------------------------------------------------------------------------
if input_mode == "Live Stream" and webrtc_ctx is not None and webrtc_ctx.state.playing:
    try:
        requests.get(BACKEND_URL, timeout=2)
    except Exception:
        st.error("Backend offline. Launch it with: `uvicorn backend.main:app --reload --port 8000`")
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
        
        if frame_num % 5 == 0:
            fire_triggered = process_frame_logic(frame, frame_num)
            render_alerts(st.session_state.alerts)
            
        time.sleep(0.01)
        
    if fire_triggered:
        st.warning("⚠️ Critical fire hazard confirmed. Evacuation routing active above.")
