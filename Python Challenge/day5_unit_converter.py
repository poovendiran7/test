import streamlit as st

# Page config
st.set_page_config(page_title="🌍 Smart Unit Converter", layout="centered")

# Global Styling: Black background, white text
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
        font-weight: bold;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Tabs instead of sidebar
tab1, tab2, tab3, tab4 = st.tabs(["💰 Currency", "🌡️ Temperature", "📏 Length", "⚖️ Weight"])

# ---------------------- CURRENCY ----------------------
with tab1:
    st.header("💰 Currency Converter (Static Rates)")

    # Static rates against USD
    rates = {
        "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 147.0, "CNY": 7.3,
        "AUD": 1.56, "CAD": 1.34, "CHF": 0.89, "SGD": 1.35, "MYR": 4.68,
        "INR": 83.2, "KRW": 1330.0, "THB": 36.3, "HKD": 7.82, "NZD": 1.67
    }

    currencies = list(rates.keys())

    col1, col2 = st.columns(2)
    with col1:
        from_currency = st.selectbox("From Currency", currencies, index=0)
        from_amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.1, key="from_amt")
    with col2:
        to_currency = st.selectbox("To Currency", currencies, index=1)

    # Conversion using static rates
    result = from_amount * (rates[to_currency] / rates[from_currency])
    st.success(f"{from_amount:.2f} {from_currency} = {result:.2f} {to_currency}")

# ---------------------- TEMPERATURE ----------------------
with tab2:
    st.header("🌡️ Temperature Converter")

    # Initialize session state
    if "celsius" not in st.session_state:
        st.session_state.celsius = 0.0
    if "fahrenheit" not in st.session_state:
        st.session_state.fahrenheit = 32.0
    if "last_temp" not in st.session_state:
        st.session_state.last_temp = "C"

    def update_celsius():
        st.session_state.last_temp = "C"
        st.session_state.fahrenheit = round((st.session_state.celsius * 9/5) + 32, 2)

    def update_fahrenheit():
        st.session_state.last_temp = "F"
        st.session_state.celsius = round((st.session_state.fahrenheit - 32) * 5/9, 2)

    col1, col2 = st.columns(2)
    col1.number_input("Celsius (°C)", key="celsius", step=0.1, on_change=update_celsius)
    col2.number_input("Fahrenheit (°F)", key="fahrenheit", step=0.1, on_change=update_fahrenheit)

    st.write(f"✅ {st.session_state.celsius:.2f} °C = {st.session_state.fahrenheit:.2f} °F")

# ---------------------- LENGTH ----------------------
with tab3:
    st.header("📏 Length Converter")

    options = {"Meters": 1, "Inches": 39.3701, "Feet": 3.28084, "Centimeters": 100}
    units = list(options.keys())

    col_center = st.columns([1, 2, 1])[1]  # Center the input
    with col_center:
        from_unit = st.radio("From Unit", units, horizontal=True, index=0, key="len_from")
        to_unit = st.radio("To Unit", units, horizontal=True, index=1, key="len_to")
        from_val = st.number_input(f"Enter {from_unit}", value=1.0, step=0.1, key="len_val")
        to_val = from_val * (options[to_unit] / options[from_unit])

    st.success(f"{from_val} {from_unit} = {to_val:.4f} {to_unit}")

# ---------------------- WEIGHT ----------------------
with tab4:
    st.header("⚖️ Weight Converter")

    # Initialize session state
    if "kg" not in st.session_state:
        st.session_state.kg = 1.0
    if "lb" not in st.session_state:
        st.session_state.lb = 2.20462
    if "last_weight" not in st.session_state:
        st.session_state.last_weight = "kg"

    def update_kg():
        st.session_state.last_weight = "kg"
        st.session_state.lb = round(st.session_state.kg * 2.20462, 2)

    def update_lb():
        st.session_state.last_weight = "lb"
        st.session_state.kg = round(st.session_state.lb / 2.20462, 2)

    col1, col2 = st.columns(2)
    col1.number_input("Kilograms (kg)", key="kg", step=0.1, on_change=update_kg)
    col2.number_input("Pounds (lb)", key="lb", step=0.1, on_change=update_lb)

    st.write(f"✅ {st.session_state.kg:.2f} kg = {st.session_state.lb:.2f} lb")
