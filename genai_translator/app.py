# meeting_translator_app.py

import streamlit as st
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize ChatOpenAI
llm = ChatOpenAI(model_name="gpt-4", temperature=0.4, openai_api_key=OPENAI_API_KEY)

# App UI setup
st.set_page_config(page_title="Meeting Notes to Tamil", layout="centered")
st.title("📋 Meeting Notes Translator")
st.subheader("Upload meeting notes to get a simplified Tamil summary")

# PDF text extraction
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# LLM-based summarization and translation
def summarize_and_translate(text):
    messages = [
        SystemMessage(
            content=(
                "You are a professional meeting assistant. Simplify the given meeting notes into clear, bullet-point summaries "
                "in professional language. Then translate the summary into Tamil. Output only the Tamil translation."
            )
        ),
        HumanMessage(content=text)
    ]
    response = llm(messages)
    return response.content.strip()

# Input choice
input_type = st.radio("Choose input type", ("Text", "PDF"))

input_text = ""
if input_type == "Text":
    input_text = st.text_area("Enter meeting minutes (in English):", height=300)
elif input_type == "PDF":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file:
        input_text = extract_text_from_pdf(uploaded_file)
        st.text_area("Extracted Text from PDF:", input_text, height=300)

# Process button
if input_text:
    if st.button("🔁 Summarize and Translate"):
        with st.spinner("Processing with GPT-4..."):
            tamil_summary = summarize_and_translate(input_text)
            st.success("✅ Translation complete!")
            st.subheader("📝 Tamil Summary:")
            st.text_area("Output (Tamil):", tamil_summary, height=300)
            st.download_button("📥 Download Summary", tamil_summary, file_name="tamil_summary.txt")
