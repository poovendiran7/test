import streamlit as st
import datetime
import plotly.graph_objects as go

# ---------------- CONFIG ----------------
st.set_page_config(page_title="💧 Hydration Tracker", layout="centered")

DAILY_GOAL_LITRES = 3.0
GLASS_SIZE_LITRES = 0.25  # 1 glass = 250 ml

# ---------------- STATE ----------------
if "intake" not in st.session_state:
    st.session_state.intake = {}  # {date_str: litres}

# Get today's date
today = datetime.date.today()
today_str = today.strftime("%Y-%m-%d")

if today_str not in st.session_state.intake:
    st.session_state.intake[today_str] = 0.0

# ---------------- FUNCTIONS ----------------
def add_water(amount):
    st.session_state.intake[today_str] += amount

def remove_water(amount):
    st.session_state.intake[today_str] = max(0, st.session_state.intake[today_str] - amount)

# ---------------- UI ----------------
st.title("💧 Daily Hydration Tracker")

st.subheader(f"📅 {today.strftime('%A, %d %B %Y')}")

# Buttons for input
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("+1 Glass"):
        add_water(GLASS_SIZE_LITRES)
with col2:
    if st.button("-1 Glass"):
        remove_water(GLASS_SIZE_LITRES)
with col3:
    if st.button("+0.5 L"):
        add_water(0.5)
with col4:
    if st.button("-0.5 L"):
        remove_water(0.5)

# ---------------- DAILY PROGRESS ----------------
today_intake = st.session_state.intake[today_str]
progress = min(today_intake / DAILY_GOAL_LITRES, 1.0)

# Progress bar with color indicator
if progress < 0.33:
    bar_color = "red"
elif progress < 0.66:
    bar_color = "orange"
elif progress < 1:
    bar_color = "blue"
else:
    bar_color = "green"

st.markdown(
    f"""
    <div style="border-radius:10px;background-color:#333;padding:10px">
    <div style="width:100%;background-color:#555;height:30px;border-radius:10px;">
        <div style="width:{progress*100:.1f}%;background-color:{bar_color};height:30px;border-radius:10px;"></div>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(f"💧 {today_intake:.2f} L / {DAILY_GOAL_LITRES} L")

# Celebration if goal reached
if today_intake >= DAILY_GOAL_LITRES:
    st.balloons()
    st.success("🎉 Congratulations! You achieved your daily hydration goal!")

# ---------------- WEEKLY CHART ----------------
st.subheader("📊 Weekly Hydration Chart")

# Collect last 7 days
dates = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
intakes = [st.session_state.intake.get(d, 0.0) for d in dates]

# Interactive Plotly chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=dates,
    y=intakes,
    marker_color="skyblue",
    name="Daily Intake",
    hovertemplate="%{x}<br>💧 %{y:.2f} L<extra></extra>"
))

# Add daily goal line
fig.add_hline(
    y=DAILY_GOAL_LITRES,
    line_dash="dash",
    line_color="green",
    annotation_text="Daily Goal (3L)",
    annotation_position="top left"
)

fig.update_layout(
    title="Weekly Hydration (Last 7 Days)",
    xaxis_title="Date",
    yaxis_title="Litres",
    template="plotly_dark",
    bargap=0.3
)

st.plotly_chart(fig, use_container_width=True)
