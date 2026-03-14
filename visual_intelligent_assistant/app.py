import streamlit as st
import os
from openai import OpenAI
import pandas as pd
from PIL import Image
from PyPDF2 import PdfReader
import speech_recognition as sr

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(page_title="Visual Intelligent Assistant")

st.title("🧠 Visual Intelligent Assistant")
st.write("Chat | Image | Audio | Files")

# ---------------------------
# OPENAI API KEY
# ---------------------------

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI API key not found. Please set OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

MODEL = "gpt-4o-mini"

# ---------------------------
# CHAT SECTION
# ---------------------------

st.header("💬 Chat with AI")

user_prompt = st.text_input("Ask something")

if st.button("Send") and user_prompt:

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    st.success(response.choices[0].message.content)

# ---------------------------
# IMAGE UPLOAD
# ---------------------------

st.header("🖼 Image Upload")

image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if image_file:

    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image")

    st.info("Image uploaded successfully.")

# ---------------------------
# FILE UPLOAD
# ---------------------------

st.header("📄 File Upload")

file = st.file_uploader("Upload PDF / CSV / TXT")

if file:

    if file.type == "application/pdf":

        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        st.text_area("Extracted Text", text[:2000])

    elif file.type == "text/csv":

        df = pd.read_csv(file)
        st.dataframe(df)

    elif file.type == "text/plain":

        text = file.read().decode()
        st.text(text)

# ---------------------------
# AUDIO UPLOAD
# ---------------------------

st.header("🎤 Audio Upload")

audio_file = st.file_uploader("Upload WAV audio", type=["wav"])

if audio_file:

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)

        st.write("Transcription:", text)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": text}
            ]
        )

        st.success(response.choices[0].message.content)

    except:
        st.error("Could not recognize audio")