import streamlit as st
import speech_recognition as sr
import os
import matplotlib.pyplot as plt
from sentiment import get_sentiment
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Sentiment Analyzer", layout="wide")

# ---------- DARK STYLE ----------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
</style>
""", unsafe_allow_html=True)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- SESSION STATE ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- SIDEBAR ----------
st.sidebar.title("📌 Project Info")
st.sidebar.info("""
AI-powered helpdesk sentiment analyzer  
Supports audio + text + live mic
""")

mode = st.sidebar.selectbox(
    "Choose Input Mode",
    ["Upload Audio", "Live Microphone", "Text Input"]
)

# ---------- TITLE ----------
st.markdown("<h1 style='text-align:center;'>📞 Helpdesk Sentiment Dashboard</h1>", unsafe_allow_html=True)

# ---------- FUNCTION ----------
def analyze_text(text):
    sentiment, emoji, polarity = get_sentiment(text)

    st.subheader("📝 Transcription / Text")
    st.write(text)

    col1, col2, col3 = st.columns(3)
    col1.metric("Sentiment", sentiment)
    col2.metric("Polarity", round(polarity, 2))
    col3.metric("Confidence", f"{abs(polarity)*100:.1f}%")

    if sentiment == "Positive":
        st.success(f"😊 Positive")
    elif sentiment == "Negative":
        st.error(f"😡 Negative")
    else:
        st.warning(f"😐 Neutral")

    st.progress(min(max((polarity + 1)/2, 0), 1))

    # Save history
    st.session_state.history.append({
        "text": text,
        "sentiment": sentiment,
        "polarity": polarity
    })

# ---------- MODE 1: AUDIO ----------
if mode == "Upload Audio":
    uploaded_file = st.file_uploader("Upload WAV File", type=["wav"])

    if uploaded_file:
        st.audio(uploaded_file)

        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        recognizer = sr.Recognizer()

        with st.spinner("Analyzing..."):
            with sr.AudioFile(file_path) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data)
                    analyze_text(text)
                except:
                    st.error("Audio not clear")

# ---------- MODE 2: LIVE MIC ----------
elif mode == "Live Microphone":
    if st.button("🎙 Start Recording"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Speak now...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                analyze_text(text)
            except:
                st.error("Could not understand")

# ---------- MODE 3: TEXT ----------
elif mode == "Text Input":
    user_text = st.text_area("Enter text")

    if st.button("Analyze"):
        analyze_text(user_text)

# ---------- HISTORY DASHBOARD ----------
if st.session_state.history:
    st.subheader("📊 Sentiment Timeline")

    df = pd.DataFrame(st.session_state.history)

    st.line_chart(df["polarity"])

    st.subheader("📈 Comparison Table")
    st.dataframe(df)
