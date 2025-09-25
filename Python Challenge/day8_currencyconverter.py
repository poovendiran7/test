import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(page_title="💱 Currency Converter", layout="centered")

# Always dark theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- CURRENCIES ----------------
currencies = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "AUD": "A$",
    "CAD": "C$",
    "CHF": "CHF",
    "CNY": "¥",
    "HKD": "HK$",
    "SGD": "S$",
    "NZD": "NZ$",
    "SEK": "kr",
    "NOK": "kr",
    "INR": "₹",
    "KRW": "₩",
}
currency_list = list(currencies.keys())

# Static prefetched conversion rates (against 1 USD)
static_rates = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 146.2,
    "AUD": 1.55,
    "CAD": 1.36,
    "CHF": 0.88,
    "CNY": 7.28,
    "HKD": 7.82,
    "SGD": 1.35,
    "NZD": 1.67,
    "SEK": 10.85,
    "NOK": 10.60,
    "INR": 83.1,
    "KRW": 1330.0,
}


def convert(amount: float, from_curr: str, to_curr: str) -> float:
    """Convert using static prefetched rates (base: USD)."""
    if from_curr == to_curr:
        return round(amount, 8)
    usd_value = amount / static_rates[from_curr]  # convert to USD
    return round(usd_value * static_rates[to_curr], 8)


# ---------------- SESSION STATE INITIALIZATION ----------------
if "from_currency" not in st.session_state:
    st.session_state["from_currency"] = "USD"
if "to_currency" not in st.session_state:
    st.session_state["to_currency"] = "EUR"

if "from_value" not in st.session_state:
    st.session_state["from_value"] = 1.0
if "to_value" not in st.session_state:
    st.session_state["to_value"] = convert(
        st.session_state["from_value"],
        st.session_state["from_currency"],
        st.session_state["to_currency"],
    )


# ---------------- CALLBACKS ----------------
def update_to():
    """Called when from_value or currency changes: compute to_value from from_value."""
    f = st.session_state["from_value"]
    fc = st.session_state["from_currency"]
    tc = st.session_state["to_currency"]
    st.session_state["to_value"] = round(convert(f, fc, tc), 2)


def update_from():
    """Called when to_value changes: compute from_value from to_value."""
    t = st.session_state["to_value"]
    fc = st.session_state["from_currency"]
    tc = st.session_state["to_currency"]
    st.session_state["from_value"] = round(convert(t, tc, fc), 2)


# ---------------- UI ----------------
st.title("💱 Instant Currency Converter")

col1, col2 = st.columns(2)

with col1:
    st.selectbox(
        "From Currency",
        currency_list,
        key="from_currency",
        on_change=update_to,
    )

    st.number_input(
        label=f"Amount in {st.session_state['from_currency']} ({currencies[st.session_state['from_currency']]})",
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key="from_value",
        on_change=update_to,
    )

with col2:
    st.selectbox(
        "To Currency",
        currency_list,
        key="to_currency",
        on_change=update_to,
    )

    st.number_input(
        label=f"Amount in {st.session_state['to_currency']} ({currencies[st.session_state['to_currency']]})",
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key="to_value",
        on_change=update_from,
    )

# ---------------- DISPLAY ----------------
rate = convert(1, st.session_state["from_currency"], st.session_state["to_currency"])
st.metric(
    label=f"💹 1 {st.session_state['from_currency']} = {rate:.4f} {st.session_state['to_currency']}",
    value=f"{currencies[st.session_state['from_currency']]}{st.session_state['from_value']} ➝ "
          f"{currencies[st.session_state['to_currency']]}{st.session_state['to_value']}",
)
