import streamlit as st

st.title("🍽️ Bill Splitter App")

# Step 1: Get total bill and number of people
total_amount = st.number_input("Enter total bill amount (RM)", min_value=0.0, step=1.0)
num_people = st.number_input("Enter number of people", min_value=1, step=1)

st.write("---")

# Step 2: Add optional names and contributions
st.subheader("👥 Contributions")
names = []
contributions = []

for i in range(int(num_people)):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"Name of person {i+1}", key=f"name_{i}")
        if not name.strip():
            name = f"Person {i+1}"  # fallback if name not provided
    with col2:
        contribution = st.number_input(
            f"Contribution by {name}", min_value=0.0, step=1.0, key=f"contrib_{i}"
        )
    names.append(name)
    contributions.append(contribution)

st.write("---")

# Step 3: Calculate split
if st.button("💰 Calculate Split"):
    if total_amount <= 0:
        st.warning("⚠️ Please enter a valid total amount.")
    elif num_people <= 0:
        st.warning("⚠️ Please enter a valid number of people.")
    else:
        fair_share = total_amount / num_people
        st.subheader("📊 Results")
        st.write(f"Each person should ideally pay: **RM {fair_share:.2f}**")

        results = []
        for name, contrib in zip(names, contributions):
            balance = contrib - fair_share
            if balance > 0:
                results.append(f"✅ {name} should get back **RM {balance:.2f}**")
            elif balance < 0:
                results.append(f"❌ {name} should pay **RM {abs(balance):.2f}** more")
            else:
                results.append(f"👌 {name} is settled.")

        for r in results:
            st.write(r)