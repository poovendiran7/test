import streamlit as st

# Mapping of alphabets to numerology values
numerology_map = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 8,
    "G": 3, "H": 5, "I": 1, "J": 1, "K": 2, "L": 3,
    "M": 4, "N": 5, "O": 7, "P": 8, "Q": 1, "R": 2,
    "S": 3, "T": 4, "U": 6, "V": 6, "W": 6, "X": 5,
    "Y": 1, "Z": 7
}

def calculate_value(input_text: str):
    """Convert text into numerology value with steps."""
    breakdown = []
    total = 0

    # Step 1: Assign values
    for char in input_text.upper():
        if char.isalpha():  
            val = numerology_map.get(char, 0)
            breakdown.append(f"{char}={val}")
            total += val
        elif char.isdigit():  
            val = int(char)
            breakdown.append(f"{char}={val}")
            total += val
        # ignore spaces and other symbols

    steps = []
    steps.append(f"Step 1: Breakdown → {' + '.join(breakdown)} = {total}")

    # Step 2: Reduce to single digit if needed
    while total > 9:
        digits = [int(d) for d in str(total)]
        step_str = " + ".join(str(d) for d in digits)
        total = sum(digits)
        steps.append(f"Step 2: {step_str} = {total}")

    return total, steps


# --- Streamlit UI ---
st.title("🔢 Numerology Calculator")

user_input = st.text_input("Enter text or numbers:", "")

if st.button("Calculate"):
    if user_input.strip():
        result, steps = calculate_value(user_input)

        st.subheader("📝 Calculation Steps")
        for s in steps:
            st.write(s)

        st.success(f"✨ Final Numerology Value for '{user_input}': **{result}**")
    else:
        st.warning("⚠️ Please enter some text or numbers.")
