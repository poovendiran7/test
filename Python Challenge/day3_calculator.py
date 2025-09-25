import streamlit as st
import time

# --- Page Config ---
st.set_page_config(page_title="Calculator", page_icon="🚀", layout="centered")

# --- Futuristic Styling ---
st.markdown("""
    <style>
    body {
        background-color: #0d0d0d;
        color: #00f0ff;
        font-family: 'Orbitron', sans-serif;
    }
    .result-box {
        font-size: 40px;
        font-weight: bold;
        color: #0ff;
        text-shadow: 0 0 10px #0ff, 0 0 20px #0ff, 0 0 40px #0ff;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #0ff;
        text-align: center;
        margin-top: 20px;
    }
    .stButton button {
        background: linear-gradient(90deg, #00f0ff, #0077ff);
        border: none;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #0077ff, #00f0ff);
        transform: scale(1.1);
        box-shadow: 0 0 20px #00f0ff;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align: center; color:#00f0ff;'>🚀 Calculator</h1>", unsafe_allow_html=True)

# --- Inputs ---
num1 = st.number_input("Enter first number:", format="%.2f")
num2 = st.number_input("Enter second number:", format="%.2f")

operation = st.selectbox("Choose operation:", ["➕ Add", "➖ Subtract", "✖ Multiply", "➗ Divide"])

if st.button("⚡ Calculate"):
    with st.spinner("⚙️ Initializing quantum processors..."):
        time.sleep(1.5)  # fake futuristic loading delay

    result = None
    if "Add" in operation:
        result = num1 + num2
    elif "Subtract" in operation:
        result = num1 - num2
    elif "Multiply" in operation:
        result = num1 * num2
    elif "Divide" in operation:
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("❌ Cannot divide by zero!")

    if result is not None:
        st.markdown(f"<div class='result-box'>✨ Result: {result:.2f}</div>", unsafe_allow_html=True)
