import streamlit as st
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="🍔 Restaurant Order & Billing App", layout="wide")

# ----------------- MENU -----------------
MENU = {
    "🍔 Burger": 8.5,
    "🍕 Pizza": 12.0,
    "🥗 Salad": 7.0,
    "🥤 Soda": 2.5,
    "🍟 Fries": 3.5,
    "🍦 Ice Cream": 4.0,
}

TAX_RATE = 0.06  # 6% tax

# ----------------- SESSION STATE -----------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ----------------- FUNCTIONS -----------------
def add_to_cart(item, qty):
    if item in st.session_state.cart:
        st.session_state.cart[item] += qty
    else:
        st.session_state.cart[item] = qty

def remove_from_cart(item):
    if item in st.session_state.cart:
        del st.session_state.cart[item]

def generate_invoice_csv(cart):
    df = pd.DataFrame([(item, qty, MENU[item], qty * MENU[item]) for item, qty in cart.items()],
                      columns=["Item", "Quantity", "Price", "Total"])
    df.loc["Subtotal"] = ["", "", "", df["Total"].sum()]
    df.loc["Tax (6%)"] = ["", "", "", df["Total"].sum() * TAX_RATE]
    df.loc["Grand Total"] = ["", "", "", df["Total"].sum() * (1 + TAX_RATE)]
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def generate_invoice_pdf(cart):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "🍔 Restaurant Invoice 🍕")

    c.setFont("Helvetica", 12)
    y = height - 100
    c.drawString(50, y, "Item")
    c.drawString(250, y, "Qty")
    c.drawString(300, y, "Price")
    c.drawString(400, y, "Total")
    y -= 20

    subtotal = 0
    for item, qty in cart.items():
        price = MENU[item]
        total = qty * price
        c.drawString(50, y, item)
        c.drawString(250, y, str(qty))
        c.drawString(300, y, f"${price:.2f}")
        c.drawString(400, y, f"${total:.2f}")
        subtotal += total
        y -= 20

    tax = subtotal * TAX_RATE
    grand_total = subtotal + tax

    y -= 20
    c.drawString(300, y, "Subtotal:")
    c.drawString(400, y, f"${subtotal:.2f}")
    y -= 20
    c.drawString(300, y, "Tax (6%):")
    c.drawString(400, y, f"${tax:.2f}")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, y, "Total:")
    c.drawString(400, y, f"${grand_total:.2f}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ----------------- APP UI -----------------
st.title("🍔 Restaurant Order & Billing App")
st.write("Select your favorite meals and generate a bill instantly! 🎉")

menu_col, cart_col = st.columns(2)

# ----- MENU -----
with menu_col:
    st.subheader("📋 Menu")
    for item, price in MENU.items():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{item}** - ${price:.2f}")
        with col2:
            qty = st.number_input(f"Qty {item}", min_value=1, max_value=10, value=1, key=f"qty_{item}")
        with col3:
            if st.button(f"Add {item}", key=f"btn_{item}"):
                add_to_cart(item, qty)
                st.success(f"✅ Added {qty} x {item} to cart")

# ----- CART -----
with cart_col:
    st.subheader("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        df_cart = pd.DataFrame(
            [(item, qty, MENU[item], qty * MENU[item]) for item, qty in st.session_state.cart.items()],
            columns=["Item", "Quantity", "Price", "Total"]
        )
        st.table(df_cart)

        subtotal = df_cart["Total"].sum()
        tax = subtotal * TAX_RATE
        total = subtotal + tax

        st.metric("Subtotal", f"${subtotal:.2f}")
        st.metric("Tax (6%)", f"${tax:.2f}")
        st.metric("Grand Total", f"${total:.2f}")

        # Download buttons
        csv_data = generate_invoice_csv(st.session_state.cart)
        st.download_button("📥 Download Invoice (CSV)", data=csv_data, file_name="invoice.csv", mime="text/csv")

        pdf_data = generate_invoice_pdf(st.session_state.cart)
        st.download_button("📥 Download Invoice (PDF)", data=pdf_data, file_name="invoice.pdf", mime="application/pdf")
