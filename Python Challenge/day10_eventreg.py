import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Event Registration System 🎉", layout="wide")

# Initialize session storage
if "registrations" not in st.session_state:
    st.session_state.registrations = []

st.title("🎉 Event Registration System")

# Tabs for User & Admin
tabs = st.tabs(["📝 Register", "📊 Admin Panel"])

# ================== USER REGISTRATION ==================
with tabs[0]:
    st.header("Register for an Event")
    st.write("Fill in your details below 👇")

    with st.form("registration_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        event_choice = st.radio("Choose Event", ["Morning", "Afternoon", "Evening"])
        submit = st.form_submit_button("Register ✅")

    if submit:
        if not name or not email:
            st.warning("⚠️ Please provide both name and email.")
        else:
            # Save registration
            st.session_state.registrations.append({
                "Name": name,
                "Email": email,
                "Event": event_choice
            })
            st.success(f"🎉 Thank you {name}! You have registered for the {event_choice} event.")

    # Show current total
    st.metric("Total Registrations", len(st.session_state.registrations))


# ================== ADMIN PANEL ==================
with tabs[1]:
    st.header("📊 Admin Panel")
    st.write("Here you can view registrations and download them as CSV.")

    if len(st.session_state.registrations) == 0:
        st.info("No registrations yet.")
    else:
        df = pd.DataFrame(st.session_state.registrations)

        # Show table
        st.dataframe(df, use_container_width=True)

        # Show counts by event
        counts = df["Event"].value_counts().reset_index()
        counts.columns = ["Event", "Registrations"]
        st.bar_chart(counts.set_index("Event"))

        # Export to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Registrations as CSV",
            data=csv_buffer.getvalue(),
            file_name="registrations.csv",
            mime="text/csv",
        )
