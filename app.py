import streamlit as st
import yt_dlp
import os
import uuid
import json

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Universal Video Downloader",
    page_icon="⬇️",
    layout="centered"
)

DOWNLOAD_DIR = "downloads"
HISTORY_FILE = "history.json"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

# ---------------- THEME ----------------
theme = st.sidebar.toggle("🌙 Dark Mode")

# Enhanced Styling CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Poppins', sans-serif;
}

.main .block-container {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    padding: 2.5rem;
    margin-top: 2rem;
}

.sidebar .sidebar-content {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin: 1rem;
    padding: 1rem;
}

/* Title Styling */
h1 {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-weight: 700;
    font-size: 2.5rem !important;
    margin-bottom: 0.5rem;
}

/* Button Styling */
.stButton > button {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

/* Input Styling */
.stTextInput > div > div > input {
    background: rgba(59, 130, 246, 0.3) !important;
    border: 2px solid rgba(59, 130, 246, 0.5) !important;
    border-radius: 15px;
    color: white !important;
    font-size: 1.1rem;
    padding: 0.75rem 1rem;
    backdrop-filter: blur(10px);
}

.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.4) !important;
    background: rgba(59, 130, 246, 0.4) !important;
}

/* Enhanced Selectbox Styling - Working Dropdown */
.stSelectbox > div > div > div[data-baseweb="select"] {
    background: rgba(255, 255, 255, 0.15) !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 15px !important;
    backdrop-filter: blur(15px) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}

.stSelectbox > div > div > div[data-baseweb="select"]:hover {
    border-color: #4ecdc4 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2) !important;
}

.stSelectbox > div > div > div[data-baseweb="select"] > div {
    color: white !important;
    font-weight: 500 !important;
    padding: 0.75rem 1rem !important;
    cursor: pointer !important;
}

/* Only hide text input, keep dropdown functional */
.stSelectbox input[type="text"] {
    opacity: 0 !important;
    position: absolute !important;
    z-index: -1 !important;
}

/* Keep dropdown clickable */
.stSelectbox div[role="combobox"] {
    cursor: pointer !important;
}

/* Dropdown Menu Styling */
.stSelectbox div[data-baseweb="popover"] {
    margin-top: 5px !important;
    border-radius: 15px !important;
    backdrop-filter: blur(20px) !important;
    background: rgba(30, 30, 30, 0.95) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3) !important;
}

.stSelectbox div[data-baseweb="popover"] ul {
    background: transparent !important;
    border-radius: 15px !important;
    padding: 0.5rem !important;
}

.stSelectbox div[data-baseweb="popover"] li {
    background: transparent !important;
    color: white !important;
    padding: 0.75rem 1rem !important;
    border-radius: 10px !important;
    margin: 0.2rem 0 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.stSelectbox div[data-baseweb="popover"] li:hover {
    background: rgba(78, 205, 196, 0.2) !important;
    color: #4ecdc4 !important;
}

.stSelectbox div[data-baseweb="popover"] li[aria-selected="true"] {
    background: rgba(255, 107, 107, 0.2) !important;
    color: #ff6b6b !important;
}

/* Arrow Icon Styling */
.stSelectbox svg {
    color: white !important;
    transition: all 0.3s ease !important;
}

.stSelectbox > div > div > div[data-baseweb="select"]:hover svg {
    color: #4ecdc4 !important;
    transform: rotate(180deg) !important;
}

/* Label Enhancement */
.stSelectbox > label {
    color: white !important;
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    margin-bottom: 0.5rem !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
}

/* Radio Button Styling - Better Horizontal Layout */
.stRadio > div {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
    justify-content: flex-start;
}

.stRadio > div > label {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 20px !important;
    padding: 0.5rem 0.8rem !important;
    color: white !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-width: fit-content !important;
    font-size: 0.9rem !important;
    white-space: nowrap !important;
}

.stRadio > div > label:hover {
    background: rgba(78, 205, 196, 0.2) !important;
    border-color: #4ecdc4 !important;
    transform: translateY(-2px) scale(1.05) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
}

.stRadio > div > label[data-checked="true"] {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4) !important;
    border-color: transparent !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
    transform: scale(1.05) !important;
}

/* Hide radio circles */
.stRadio input[type="radio"] {
    display: none !important;
}



/* Progress Bar */
.stProgress > div > div > div {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
    border-radius: 10px;
}

/* Alert Styling */
.stAlert {
    border-radius: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Download Button */
.stDownloadButton > button {
    background: linear-gradient(45deg, #4ecdc4, #44a08d);
    color: white;
    border: none;
    border-radius: 20px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

/* History Section */
.stSubheader {
    color: white;
    font-weight: 600;
    text-align: center;
}

/* Sidebar Title */
.sidebar .sidebar-content h2 {
    color: white;
    text-align: center;
    font-weight: 600;
    margin-bottom: 1.5rem;
}

/* Labels */
label {
    color: white !important;
    font-weight: 500;
}

/* Caption */
.stCaption {
    text-align: center;
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Divider */
hr {
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin: 2rem 0;
}

/* History Items */
.stWrite {
    background: rgba(255, 255, 255, 0.1);
    padding: 0.5rem 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    border-left: 4px solid #4ecdc4;
}

/* Video Player Styling - Make it bigger */
video {
    max-width: 600px !important;
    max-height: 400px !important;
    width: 100% !important;
    height: auto !important;
    border-radius: 15px !important;
    margin: 1rem auto !important;
    display: block !important;
}

/* Audio Player Styling */
audio {
    max-width: 600px !important;
    width: 100% !important;
    margin: 1rem auto !important;
    display: block !important;
}

/* Hide Streamlit header elements */
.stApp > header {
    display: none !important;
}

/* Hide Deploy button and menu */
.stDeployButton {
    display: none !important;
}

/* Hide Deploy button - more specific selectors */
[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

/* Hide GitHub icon and Deploy button */
.stApp > header [data-testid="stToolbar"] {
    display: none !important;
}

/* Hide entire toolbar */
.stToolbar {
    display: none !important;
}

/* Hide three dots menu */
.stActionButton {
    display: none !important;
}

/* Hide main menu */
.stMainMenu {
    display: none !important;
}

/* Hide footer */
.stApp > footer {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

if theme:
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    }
    
    .main .block-container {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar .sidebar-content {
        background: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    h1 {
        background: linear-gradient(45deg, #ff9a9e, #fecfef, #fecfef) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    # Light mode - better visibility for download details and input field
    st.markdown("""
    <style>
    /* Light mode download progress styling */
    .download-progress {
        background: rgba(0, 0, 0, 0.8) !important;
        color: white !important;
        border: 2px solid rgba(0, 0, 0, 0.3) !important;
    }
    
    .download-progress span {
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Light mode input field styling */
    .stTextInput > div > div > input {
        background: rgba(59, 130, 246, 0.4) !important;
        border: 2px solid rgba(59, 130, 246, 0.6) !important;
        color: white !important;
        font-weight: 500 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stTextInput > div > div > input:focus {
        background: rgba(59, 130, 246, 0.5) !important;
        border-color: #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.3) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.8) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- SIDEBAR - HISTORY ----------------
st.sidebar.subheader("📁 Download History")

with open(HISTORY_FILE) as f:
    history = json.load(f)

if history:
    for h in reversed(history[-3:]):  # Show only last 3
        title = h.get('title', 'Unknown')[:25] + '...' if len(h.get('title', '')) > 25 else h.get('title', 'Unknown')
        st.sidebar.write(f"**{h['platform']}** | {h['type']}")
        st.sidebar.caption(f"{title} ({h.get('size_mb', 0)} MB)")
        st.sidebar.divider()
else:
    st.sidebar.caption("No downloads yet")

# Clear History Button
if st.sidebar.button("🗑️ Clear History"):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)
    st.sidebar.success("History cleared!")
    st.rerun()

# ---------------- MAIN UI ----------------
st.markdown("""
<div style="text-align: center; margin-bottom: 1rem;">
    <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin-bottom: 0.5rem;">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="url(#gradient1)">
            <defs>
                <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#4ecdc4;stop-opacity:1" />
                </linearGradient>
            </defs>
            <path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"/>
        </svg>
        <h1 style="background: linear-gradient(45deg, #ff6b6b, #4ecdc4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; font-size: 2.5rem; font-weight: 700;">Universal Video Downloader</h1>
    </div>
    <p style="color: rgba(255, 255, 255, 0.8); font-size: 1.1rem; margin: 0;">Download, preview & save videos/audio on any device</p>
</div>
""", unsafe_allow_html=True)

# URL Input Section (Top)
st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
        <path d="M3.9,12C3.9,10.29 5.29,8.9 7,8.9H11V7H7A5,5 0 0,0 2,12A5,5 0 0,0 7,17H11V15.1H7C5.29,15.1 3.9,13.71 3.9,12M8,13H16V11H8V13M17,7H13V8.9H17C18.71,8.9 20.1,10.29 20.1,12C20.1,13.71 18.71,15.1 17,15.1H13V17H17A5,5 0 0,0 22,12A5,5 0 0,0 17,7Z"/>
    </svg>
    <span style="color: white; font-weight: 600; font-size: 1.2rem;">Paste video link</span>
</div>
""", unsafe_allow_html=True)
url = st.text_input("Paste video link", label_visibility="collapsed")

download_btn = st.button("🔍 Search")

st.divider()

# Settings Section (Bottom)
st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem; margin: 2rem 0 1rem 0;">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
        <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
    </svg>
    <h3 style="color: white; margin: 0; font-weight: 600;">Settings</h3>
</div>
""", unsafe_allow_html=True)

# First Row - Platform and Download Type
st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
        <path d="M17,12C17,9.24 14.76,7 12,7C9.24,7 7,9.24 7,12C7,14.76 9.24,17 12,17C14.76,17 17,14.76 17,12M12,1L21.5,6.5L21.5,17.5L12,23L2.5,17.5L2.5,6.5L12,1M12,21L20,16.5L20,7.5L12,3L4,7.5L4,16.5L12,21Z"/>
    </svg>
    <span style="color: white; font-weight: 600;">Platform</span>
</div>
""", unsafe_allow_html=True)
platform = st.radio(
    "Platform",
    ["TikTok", "YouTube", "Instagram", "Facebook"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem; margin: 1rem 0 0.5rem 0;">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
        <path d="M21,3H3C1.89,3 1,3.89 1,5V19A2,2 0 0,0 3,21H21A2,2 0 0,0 23,19V5C23,3.89 22.1,3 21,3M21,19H3V5H21V19M16,10L12,14L8,10H16Z"/>
    </svg>
    <span style="color: white; font-weight: 600;">Download Type</span>
</div>
""", unsafe_allow_html=True)
download_type = st.radio(
    "Download Type",
    ["Video", "Audio Only (MP3)"],
    horizontal=True,
    label_visibility="collapsed"
)

# Second Row - Quality Options (Conditional)
if download_type == "Video":
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin: 1rem 0 0.5rem 0;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
            <path d="M17,10.5V7A1,1 0 0,0 16,6H4A1,1 0 0,0 3,7V10.5H17M20,2H4C2.89,2 2,2.89 2,4V20A2,2 0 0,0 4,22H20A2,2 0 0,0 22,20V4C22,2.89 21.1,2 20,2M20,20H4V12H20V20Z"/>
        </svg>
        <span style="color: white; font-weight: 600;">Video Quality</span>
    </div>
    """, unsafe_allow_html=True)
    video_quality = st.radio(
        "Video Quality",
        ["Best", "1080p", "720p", "480p", "360p"],
        horizontal=True,
        label_visibility="collapsed"
    )
    audio_quality = "320 kbps"  # Default for video
else:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.5rem; margin: 1rem 0 0.5rem 0;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
            <path d="M12,3V12.26C11.5,12.09 11,12 10.5,12C8,12 6,14 6,16.5C6,19 8,21 10.5,21C13,21 15,19 15,16.5V6H19V3H12Z"/>
        </svg>
        <span style="color: white; font-weight: 600;">Audio Quality</span>
    </div>
    """, unsafe_allow_html=True)
    audio_quality = st.radio(
        "Audio Quality",
        ["320 kbps", "192 kbps", "128 kbps"],
        horizontal=True,
        label_visibility="collapsed"
    )
    video_quality = "Best"  # Default for audio

# ---------------- HELPERS ----------------
video_format_map = {
    "Best": "best[height>=720]/best",
    "1080p": "best[height>=1080]/best[height>=720]/best",
    "720p": "best[height>=720]/best[height>=480]/best",
    "480p": "best[height>=480]/best[height>=360]/best",
    "360p": "best[height>=360]/best"
}

audio_quality_map = {
    "320 kbps": "320",
    "192 kbps": "192",
    "128 kbps": "128"
}

platform_domains = {
    "TikTok": ["tiktok.com", "douyin.com"],
    "YouTube": ["youtube.com", "youtu.be"],
    "Instagram": ["instagram.com"],
    "Facebook": ["facebook.com", "fb.watch"]
}

# Custom progress hook for yt-dlp with time estimation
import time
download_start_time = None

# Format time function
def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds//60)}m {int(seconds%60)}s"
    else:
        return f"{int(seconds//3600)}h {int((seconds%3600)//60)}m"

def progress_hook(d):
    global download_start_time
    
    if d['status'] == 'downloading':
        if download_start_time is None:
            download_start_time = time.time()
        
        if 'total_bytes' in d:
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            total_bytes = d['total_bytes']
        elif 'total_bytes_estimate' in d:
            percent = d['downloaded_bytes'] / d['total_bytes_estimate'] * 100
            total_bytes = d['total_bytes_estimate']
        else:
            percent = 0
            total_bytes = 0
        
        # Calculate time estimates
        elapsed_time = time.time() - download_start_time
        if percent > 0 and elapsed_time > 0:
            estimated_total_time = elapsed_time * (100 / percent)
            remaining_time = estimated_total_time - elapsed_time
        else:
            remaining_time = 0
        
        # Update progress bar and status
        progress_bar.progress(min(int(percent), 99))
        
        # Update status with detailed info including time
        if 'speed' in d and d['speed'] and remaining_time > 0:
            speed_mb = d['speed'] / (1024 * 1024)
            downloaded_mb = d['downloaded_bytes'] / (1024 * 1024)
            total_mb = total_bytes / (1024 * 1024) if total_bytes > 0 else 0
            
            status_text.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 15px; backdrop-filter: blur(10px);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="color: #4ecdc4; font-weight: 600;">⬇️ Downloading...</span>
                    <span style="color: white; font-weight: 600;">{percent:.1f}%</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: rgba(255,255,255,0.8); margin-bottom: 0.5rem;">
                    <span>📊 {downloaded_mb:.1f} MB / {total_mb:.1f} MB</span>
                    <span>🚀 {speed_mb:.1f} MB/s</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                    <span>⏱️ Elapsed: {format_time(elapsed_time)}</span>
                    <span style="color: #ff6b6b; font-weight: 600;">⏳ Remaining: {format_time(remaining_time)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            status_text.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 15px; backdrop-filter: blur(10px);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="color: #4ecdc4; font-weight: 600;">⬇️ Downloading...</span>
                    <span style="color: white; font-weight: 600;">{percent:.1f}%</span>
                </div>
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.8);">
                    <span>⏱️ Calculating time...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    elif d['status'] == 'finished':
        progress_bar.progress(100)
        total_time = time.time() - download_start_time if download_start_time else 0
        status_text.success(f"✅ Download completed in {format_time(total_time) if total_time > 0 else 'unknown time'}!")
        download_start_time = None

def valid_url(link, platform):
    return any(d in link for d in platform_domains[platform])

# ---------------- DOWNLOAD ----------------
if download_btn:
    if not url:
        st.error("❌ Paste a video link")
    elif not valid_url(url, platform):
        st.error("❌ Link does not match selected platform")
    else:
        try:
            # Initialize progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.info("⏳ Fetching video info...")

            file_id = str(uuid.uuid4())
            base_path = os.path.join(DOWNLOAD_DIR, file_id)

            # Get video info first with retry mechanism
            ydl_info_opts = {
                "quiet": True,
                "socket_timeout": 60,
                "retries": 10,
                "fragment_retries": 10,
                "extractor_retries": 5,
                "http_chunk_size": 1048576,
                "prefer_insecure": False,
                "no_check_certificate": True,
                "geo_bypass": True,
                "http_headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Accept-Encoding': 'gzip,deflate',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                    'Keep-Alive': '300',
                    'Connection': 'keep-alive'
                }
            }
            with yt_dlp.YoutubeDL(ydl_info_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            filesize = info.get("filesize") or info.get("filesize_approx")

            if filesize:
                size_mb = round(filesize / (1024*1024), 2)
                st.info(f"📦 Estimated Size: {size_mb} MB")

            # Setup download options with progress hook
            if download_type == "Video":
                # Use improved format selector for HD quality
                format_selector = video_format_map[video_quality]
                
                ydl_opts = {
                    "outtmpl": f"{base_path}.%(ext)s",
                    "format": format_selector,
                    "progress_hooks": [progress_hook],
                    "quiet": True,
                    "no_warnings": True,
                    "writesubtitles": False,
                    "writeautomaticsub": False,
                    "socket_timeout": 60,
                    "retries": 15,
                    "fragment_retries": 15,
                    "extractor_retries": 5,
                    "http_chunk_size": 1048576,
                    "prefer_insecure": False,
                    "geo_bypass": True,
                    "no_check_certificate": True,
                    "continuedl": True,
                    "http_headers": {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-us,en;q=0.5',
                        'Accept-Encoding': 'gzip,deflate',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                        'Keep-Alive': '300',
                        'Connection': 'keep-alive'
                    }
                }
                ext = ".mp4"
            else:
                # Audio download without FFmpeg post-processing
                ydl_opts = {
                    "outtmpl": f"{base_path}.%(ext)s",
                    "format": "bestaudio[ext=m4a]/bestaudio/best",
                    "progress_hooks": [progress_hook],
                    "quiet": True,
                    "no_warnings": True,
                    "socket_timeout": 60,
                    "retries": 15,
                    "fragment_retries": 15,
                    "extractor_retries": 5,
                    "http_chunk_size": 1048576,
                    "prefer_insecure": False,
                    "geo_bypass": True,
                    "no_check_certificate": True,
                    "continuedl": True,
                    "http_headers": {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-us,en;q=0.5',
                        'Accept-Encoding': 'gzip,deflate',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                        'Keep-Alive': '300',
                        'Connection': 'keep-alive'
                    }
                }
                ext = ".m4a"

            # Start download with real-time progress
            status_text.info("⬇️ Starting download...")
            download_start_time = None  # Reset timer
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Find the actual downloaded file
            import glob
            possible_files = glob.glob(f"{base_path}.*")
            if possible_files:
                file_path = possible_files[0]
            else:
                file_path = base_path + ext

            if os.path.exists(file_path):
                progress_bar.progress(100)
                status_text.success("✅ Download complete - Ready to use!")

                # Preview
                if download_type == "Video":
                    st.video(file_path)
                else:
                    st.audio(file_path)

                with open(file_path, "rb") as f:
                    st.download_button(
                        "📥 Save to Device",
                        data=f,
                        file_name=os.path.basename(file_path)
                    )



                # Save history
                import datetime
                with open(HISTORY_FILE, "r+") as f:
                    history = json.load(f)
                    history.append({
                        "platform": platform,
                        "type": download_type,
                        "file": os.path.basename(file_path),
                        "url": url,
                        "quality": video_quality if download_type == "Video" else audio_quality,
                        "size_mb": round(os.path.getsize(file_path) / (1024*1024), 2) if os.path.exists(file_path) else 0,
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "title": info.get('title', 'Unknown Title')[:50] + ('...' if len(info.get('title', '')) > 50 else '')
                    })
                    f.seek(0)
                    json.dump(history, f, indent=2)
                    f.truncate()

            else:
                st.error("❌ File missing after download")

        except Exception as e:
            error_msg = str(e)
            if "getaddrinfo failed" in error_msg or "Failed to resolve" in error_msg:
                st.error("🌐 Network connection issue. Please check your internet connection and try again.")
            elif "HTTP Error 403" in error_msg:
                st.error("🚫 Access denied. The video might be private or region-blocked.")
            elif "Video unavailable" in error_msg:
                st.error("📹 Video is unavailable or has been removed.")
            elif "Unsupported URL" in error_msg:
                st.error("🔗 Unsupported URL format. Please check the link.")
            else:
                st.error(f"❌ Download failed: {error_msg}")
            
            # Clear progress on error
            if 'progress_bar' in locals():
                progress_bar.empty()
            if 'status_text' in locals():
                status_text.empty()




# ---------------- FOOTER ----------------
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem 0; border-top: 1px solid rgba(255,255,255,0.2);">
    <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">
        Developed by <span style="color: #4ecdc4; font-weight: 600;">Faraz Hussain</span>
    </p>
</div>
""", unsafe_allow_html=True)
