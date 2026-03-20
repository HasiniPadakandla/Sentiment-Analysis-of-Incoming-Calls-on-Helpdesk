import streamlit as st
import speech_recognition as sr
import os
import matplotlib.pyplot as plt
from sentiment import get_sentiment

# ---------- CONFIG ----------
st.set_page_config(page_title="Helpdesk Sentiment Analyzer", layout="wide")

UPLOAD_FOLDER = "uploads"
GRAPH_FOLDER = "graphs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)

# ---------- SIDEBAR ----------
st.sidebar.title("📌 About")
st.sidebar.info("""
This project analyzes helpdesk calls using:
- Speech Recognition
- NLP (VADER)
- Sentiment Scoring
""")

# ---------- TITLE ----------
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>
📞 Sentiment Analyser - HelpDesk
</h1>
""", unsafe_allow_html=True)

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("Upload Audio File", type=["wav"])

if uploaded_file is not None:

    # 🔊 Show Audio
    st.audio(uploaded_file, format="audio/wav")

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    recognizer = sr.Recognizer()

    # ---------- LOADING ----------
    with st.spinner("Analyzing audio..."):
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data)

                # ---------- TRANSCRIPTION ----------
                st.subheader("📝 Transcription")
                st.write(text)

                sentiment, emoji, polarity = get_sentiment(text)

                # ---------- KPI CARDS ----------
                col1, col2, col3 = st.columns(3)

                col1.metric("Sentiment", sentiment)
                col2.metric("Polarity", round(polarity, 2))
                col3.metric("Confidence", f"{abs(polarity)*100:.1f}%")

                # st.metric works well with columns for dashboards :contentReference[oaicite:0]{index=0}

                # ---------- SENTIMENT BADGE ----------
                if sentiment == "Positive":
                    st.success(f"😊 Positive Sentiment")
                elif sentiment == "Negative":
                    st.error(f"😡 Negative Sentiment")
                else:
                    st.warning(f"😐 Neutral Sentiment")

                # ---------- PROGRESS BAR ----------
                st.subheader("📊 Sentiment Strength")
                st.progress(min(max((polarity + 1)/2, 0), 1))

                # ---------- GRAPH ----------
                def plot_graph(sentiment, polarity):
                    labels = ['Positive', 'Neutral', 'Negative']
                    values = [0.5, 1, 0.5]

                    if sentiment == "Positive":
                        values = [1 + abs(polarity), 1 - abs(polarity), 0.5]
                    elif sentiment == "Negative":
                        values = [0.5, 1 - abs(polarity), 1 + abs(polarity)]

                    plt.figure(figsize=(6, 4))
                    plt.bar(labels, values, color=['green', 'yellow', 'red'])
                    plt.title("Sentiment Analysis")

                    graph_path = os.path.join(GRAPH_FOLDER, "graph.png")
                    plt.savefig(graph_path)
                    plt.close()

                    return graph_path

                graph = plot_graph(sentiment, polarity)
                st.image(graph)

                # ---------- DETAILS ----------
                with st.expander("🔍 View Detailed Info"):
                    st.write("Full Text:", text)
                    st.write("Polarity Score:", polarity)

            except sr.UnknownValueError:
                st.error("Could not understand audio")

            except sr.RequestError:
                st.error("Speech recognition service unavailable")
