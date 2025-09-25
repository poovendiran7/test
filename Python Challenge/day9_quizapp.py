import streamlit as st

# -------------------------------
# 🎯 Capital Cities Quiz Data
# -------------------------------
questions = [
    {
        "question": "What is the capital of France? 🗼",
        "options": ["Paris", "Berlin", "Madrid", "Rome"],
        "answer": "Paris",
    },
    {
        "question": "What is the capital of Japan? 🗾",
        "options": ["Seoul", "Tokyo", "Beijing", "Kyoto"],
        "answer": "Tokyo",
    },
    {
        "question": "What is the capital of Australia? 🦘",
        "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
        "answer": "Canberra",
    },
    {
        "question": "What is the capital of Canada? 🍁",
        "options": ["Toronto", "Ottawa", "Vancouver", "Montreal"],
        "answer": "Ottawa",
    },
    {
        "question": "What is the capital of Brazil? 🌴",
        "options": ["São Paulo", "Brasília", "Rio de Janeiro", "Salvador"],
        "answer": "Brasília",
    },
]

# -------------------------------
# 🎮 Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="Capital Cities Quiz 🌍", page_icon="🌍", layout="centered")

# -------------------------------
# 📝 Initialize Session State
# -------------------------------
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# -------------------------------
# 🎨 Custom Styles
# -------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
        font-family: "Comic Sans MS", cursive, sans-serif;
    }
    .question-box {
        padding: 15px;
        border-radius: 12px;
        background-color: #262730;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# 🧩 Quiz Logic
# -------------------------------
st.title("🌍 Capital Cities Quiz 🏙️")
st.write("Test your knowledge of world capitals!")

if st.session_state.current_q < len(questions):
    q = questions[st.session_state.current_q]

    # Show question
    st.markdown(f"<div class='question-box'><h4>{q['question']}</h4></div>", unsafe_allow_html=True)

    # Options
    choice = st.radio("Choose your answer:", q["options"], key=f"q{st.session_state.current_q}")

    # Next button
    if st.button("👉 Next"):
        st.session_state.answers[st.session_state.current_q] = choice
        if choice == q["answer"]:
            st.session_state.score += 1
        st.session_state.current_q += 1
        st.rerun()   # ✅ Updated API

else:
    # 🎉 Final Score
    st.subheader("🎉 Quiz Completed! 🎉")
    st.success(f"Your final score: {st.session_state.score}/{len(questions)} ✅")

    # Show results breakdown
    with st.expander("📖 Review your answers"):
        for i, q in enumerate(questions):
            user_ans = st.session_state.answers.get(i, "Not answered")
            correct = q["answer"]
            if user_ans == correct:
                st.markdown(f"**Q{i+1}: {q['question']}** ✅ Correct! ({user_ans})")
            else:
                st.markdown(f"**Q{i+1}: {q['question']}** ❌ Wrong! Your answer: {user_ans}, Correct: {correct}")

    # Reset button
    if st.button("🔄 Play Again"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answers = {}
        st.rerun()   # ✅ Updated API
