import streamlit as st

# Page config
st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

st.title("⚖️ Interactive BMI Calculator")

# Measurement options
unit_height = st.radio("Select Height Unit", ["cm", "ft-inches"], horizontal=True)
unit_weight = st.radio("Select Weight Unit", ["kg", "pounds"], horizontal=True)

# Height input
if unit_height == "cm":
    height_cm = st.slider("Height (cm)", 100, 220, 170)
    height_m = height_cm / 100
else:
    feet = st.slider("Feet", 3, 7, 5)
    inches = st.slider("Inches", 0, 11, 6)
    height_m = (feet * 12 + inches) * 0.0254

# Weight input
if unit_weight == "kg":
    weight = st.slider("Weight (kg)", 30, 150, 65)
else:
    weight_lb = st.slider("Weight (pounds)", 70, 330, 150)
    weight = weight_lb * 0.453592

# BMI calculation
bmi = round(weight / (height_m ** 2), 1)

# Result categorization
if bmi < 18.5:
    status = "Underweight"
    color = "blue"
elif bmi < 24.9:
    status = "Normal"
    color = "green"
elif bmi < 29.9:
    status = "Overweight"
    color = "orange"
else:
    status = "Obese"
    color = "red"

# Display result
st.markdown(f"### Your BMI: <span style='color:{color}'>{bmi}</span>", unsafe_allow_html=True)
st.markdown(f"**Category:** <span style='color:{color}; font-size:20px'>{status}</span>", unsafe_allow_html=True)

# Visual progress bar
progress = min(bmi / 40, 1.0)
st.progress(progress)

# Silhouette or emoji visuals
if status == "Underweight":
    st.image("https://img.icons8.com/emoji/96/person.png", caption="Underweight")
elif status == "Normal":
    st.image("https://img.icons8.com/emoji/96/person-running.png", caption="Healthy")
elif status == "Overweight":
    st.image("https://img.icons8.com/emoji/96/person-lifting-weights.png", caption="Overweight")
else:
    st.image("https://img.icons8.com/emoji/96/person-in-bed.png", caption="Obese")
