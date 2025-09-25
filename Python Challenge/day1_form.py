import streamlit as st

st.title("👋 Personalized Greeting App")

# Create a form
with st.form("greeting_form"):
    name = st.text_input("Enter your name")
    age = st.slider("Select your age", 1, 100, value=25)

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not name.strip():
            st.warning("⚠️ Please enter your name before submitting.")
        else:
            st.success(f"Hello **{name}**! 🎉 You are {age} years young!")