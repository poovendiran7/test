import streamlit as st
import time
from datetime import datetime, timedelta
import math

# Configure page
st.set_page_config(
    page_title="🦆 Stopwatch Timer",
    page_icon="⏱️",
    layout="centered"
)

# Custom CSS with animations
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@400;500;600&display=swap');
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {display: none;}
    .block-container {padding-top: 2rem !important;}
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .stopwatch-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 3rem 2rem;
        margin: 1rem auto;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        max-width: 600px;
        position: relative;
        overflow: hidden;
    }
    
    /* Animated background elements */
    .stopwatch-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
        z-index: 0;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Content wrapper */
    .content-wrapper {
        position: relative;
        z-index: 1;
    }
    
    /* Title styling */
    .stopwatch-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 5px rgba(102, 126, 234, 0.3)); }
        to { filter: drop-shadow(0 0 15px rgba(102, 126, 234, 0.6)); }
    }
    
    /* Timer display */
    .timer-display {
        font-family: 'Orbitron', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        color: #2d3748;
        text-align: center;
        margin: 2rem 0;
        padding: 1.5rem;
        background: linear-gradient(145deg, #f7fafc, #edf2f7);
        border-radius: 20px;
        box-shadow: 
            inset 8px 8px 15px #d1d9e0,
            inset -8px -8px 15px #ffffff,
            0 4px 15px rgba(0,0,0,0.1);
        position: relative;
        letter-spacing: 0.1em;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Running timer animation */
    .timer-running {
        animation: timerPulse 1s ease-in-out infinite alternate;
        color: #e53e3e;
        text-shadow: 0 0 20px rgba(229, 62, 62, 0.3);
    }
    
    @keyframes timerPulse {
        from { transform: scale(1); filter: brightness(1); }
        to { transform: scale(1.05); filter: brightness(1.1); }
    }
    
    /* Milliseconds styling */
    .milliseconds {
        font-size: 2.5rem;
        color: #718096;
        font-weight: 400;
    }
    
    /* Control buttons container */
    .controls-container {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    /* Button styling */
    .stButton > button {
        border: none !important;
        border-radius: 15px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        position: relative !important;
        overflow: hidden !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Start button */
    .start-btn button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
        color: white !important;
    }
    
    .start-btn button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.4) !important;
    }
    
    /* Stop button */
    .stop-btn button {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%) !important;
        color: white !important;
    }
    
    .stop-btn button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(245, 101, 101, 0.4) !important;
    }
    
    /* Reset button */
    .reset-btn button {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
        color: white !important;
    }
    
    .reset-btn button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(66, 153, 225, 0.4) !important;
    }
    
    /* Lap times */
    .lap-times {
        background: rgba(247, 250, 252, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
        max-height: 200px;
        overflow-y: auto;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .lap-time-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(0,0,0,0.1);
        font-family: 'Orbitron', monospace;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .lap-number {
        font-weight: 600;
        color: #4a5568;
    }
    
    .lap-time {
        font-weight: 700;
        color: #2d3748;
    }
    
    /* Duck animation container */
    .duck-container {
        position: fixed;
        bottom: 20px;
        left: 0;
        width: 100%;
        height: 80px;
        z-index: 1000;
        pointer-events: none;
        overflow: hidden;
    }
    
    .duck {
        position: absolute;
        bottom: 0;
        font-size: 3rem;
        animation: walkAcross 15s linear infinite;
        transform-origin: center;
    }
    
    @keyframes walkAcross {
        0% {
            left: -100px;
            transform: scaleX(1);
        }
        45% {
            transform: scaleX(1);
        }
        50% {
            left: calc(50% - 50px);
            transform: scaleX(-1);
        }
        95% {
            transform: scaleX(-1);
        }
        100% {
            left: calc(100% + 100px);
            transform: scaleX(-1);
        }
    }
    
    /* Duck wobble animation */
    .duck::before {
        content: '🦆';
        display: block;
        animation: waddle 0.5s ease-in-out infinite alternate;
    }
    
    @keyframes waddle {
        from { transform: rotate(-5deg) translateY(0px); }
        to { transform: rotate(5deg) translateY(-3px); }
    }
    
    /* Stats container */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-item {
        background: rgba(247, 250, 252, 0.8);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: statFloat 3s ease-in-out infinite alternate;
    }
    
    @keyframes statFloat {
        from { transform: translateY(0px); }
        to { transform: translateY(-3px); }
    }
    
    .stat-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #718096;
        margin-top: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Scrollbar styling */
    .lap-times::-webkit-scrollbar {
        width: 6px;
    }
    
    .lap-times::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
        border-radius: 3px;
    }
    
    .lap-times::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.5);
        border-radius: 3px;
    }
    
    /* Responsive design */
    @media (max-width: 600px) {
        .timer-display {
            font-size: 3rem;
        }
        
        .controls-container {
            gap: 1rem;
        }
        
        .stButton > button {
            padding: 0.6rem 1.5rem !important;
            font-size: 1rem !important;
        }
        
        .stopwatch-title {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.is_running = False
    st.session_state.lap_times = []
    st.session_state.total_laps = 0

def format_time(seconds):
    """Format time as MM:SS.ms"""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    whole_seconds = int(seconds)
    milliseconds = int((seconds - whole_seconds) * 100)
    return f"{minutes:02d}:{whole_seconds:02d}", f"{milliseconds:02d}"

def start_stopwatch():
    """Start the stopwatch"""
    if not st.session_state.is_running:
        st.session_state.start_time = time.time() - st.session_state.elapsed_time
        st.session_state.is_running = True

def stop_stopwatch():
    """Stop the stopwatch"""
    if st.session_state.is_running:
        st.session_state.elapsed_time = time.time() - st.session_state.start_time
        st.session_state.is_running = False

def reset_stopwatch():
    """Reset the stopwatch"""
    st.session_state.start_time = None
    st.session_state.elapsed_time = 0
    st.session_state.is_running = False
    st.session_state.lap_times = []
    st.session_state.total_laps = 0

def add_lap():
    """Add a lap time"""
    if st.session_state.is_running:
        current_time = time.time() - st.session_state.start_time
        st.session_state.total_laps += 1
        st.session_state.lap_times.append({
            'lap': st.session_state.total_laps,
            'time': current_time
        })

# Calculate current time
if st.session_state.is_running:
    current_time = time.time() - st.session_state.start_time
else:
    current_time = st.session_state.elapsed_time

# Format time
time_parts, ms = format_time(current_time)

# Main container
st.markdown('<div class="stopwatch-container">', unsafe_allow_html=True)
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

# Title with animation
st.markdown('<h1 class="stopwatch-title">⏱️ Stopwatch Timer</h1>', unsafe_allow_html=True)

# Timer display
timer_class = "timer-display timer-running" if st.session_state.is_running else "timer-display"
st.markdown(f'''
<div class="{timer_class}">
    {time_parts}
    <span class="milliseconds">.{ms}</span>
</div>
''', unsafe_allow_html=True)

# Control buttons
st.markdown('<div class="controls-container">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="start-btn">', unsafe_allow_html=True)
    if st.button("🚀 Start", disabled=st.session_state.is_running):
        start_stopwatch()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="stop-btn">', unsafe_allow_html=True)
    if st.button("⏸️ Stop", disabled=not st.session_state.is_running):
        stop_stopwatch()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("🔄 Reset"):
        reset_stopwatch()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="start-btn">', unsafe_allow_html=True)
    if st.button("📍 Lap", disabled=not st.session_state.is_running):
        add_lap()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Statistics
if st.session_state.elapsed_time > 0 or st.session_state.is_running:
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    
    # Total time
    st.markdown(f'''
    <div class="stat-item">
        <div class="stat-value">{time_parts.replace(":", "m ")}s</div>
        <div class="stat-label">Total Time</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Status
    status = "🔴 Running" if st.session_state.is_running else "⏸️ Stopped"
    st.markdown(f'''
    <div class="stat-item">
        <div class="stat-value">{status}</div>
        <div class="stat-label">Status</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Lap count
    st.markdown(f'''
    <div class="stat-item">
        <div class="stat-value">{st.session_state.total_laps}</div>
        <div class="stat-label">Laps</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Lap times display
if st.session_state.lap_times:
    st.markdown('<div class="lap-times">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #4a5568; margin-bottom: 1rem;">🏃‍♂️ Lap Times</h3>')
    
    for lap in reversed(st.session_state.lap_times[-10:]):  # Show last 10 laps
        lap_time_parts, lap_ms = format_time(lap['time'])
        st.markdown(f'''
        <div class="lap-time-item">
            <span class="lap-number">Lap {lap['lap']}</span>
            <span class="lap-time">{lap_time_parts}.{lap_ms}</span>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Walking duck animation
st.markdown('''
<div class="duck-container">
    <div class="duck"></div>
</div>
''', unsafe_allow_html=True)

# Auto-refresh when running
if st.session_state.is_running:
    time.sleep(0.1)
    st.rerun()

# Instructions in sidebar
with st.sidebar:
    st.markdown("## 🦆 Stopwatch Instructions")
    st.markdown("""
    **How to use:**
    - 🚀 **Start**: Begin timing
    - ⏸️ **Stop**: Pause the timer
    - 🔄 **Reset**: Clear all times
    - 📍 **Lap**: Record lap time while running
    
    **Features:**
    - ⏱️ Precision timing with milliseconds
    - 📊 Live statistics display
    - 🏃‍♂️ Lap time recording
    - 🦆 Cute walking duck animation!
    - 📱 Mobile-friendly design
    
    **Tips:**
    - Use lap function to track intervals
    - The duck walks continuously for your entertainment
    - Timer updates in real-time when running
    - All lap times are automatically saved
    """)
    
    st.markdown("---")
    
    # Fun facts about ducks
    st.markdown("## 🦆 Fun Duck Facts")
    st.markdown("""
    - Ducks have waterproof feathers
    - They can sleep with one eye open
    - Ducks have excellent vision
    - Baby ducks are called ducklings
    - They can live up to 20 years!
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; padding: 1rem;'>
    ⏱️ <strong>Stopwatch Timer v1.0</strong> | Made with ❤️ and 🦆 | Built with Streamlit
    <br><em>Watch the duck walk while you time your activities!</em>
</div>
""", unsafe_allow_html=True)