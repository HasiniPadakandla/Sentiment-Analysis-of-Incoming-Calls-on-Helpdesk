import streamlit as st
import speech_recognition as sr
import os
import matplotlib.pyplot as plt
from sentiment import get_sentiment

UPLOAD_FOLDER = "uploads"
GRAPH_FOLDER = "graphs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)

def plot_sentiment_graph(sentiment, polarity, file_name):
    labels = ['Positive', 'Neutral', 'Negative']
    colors = ['green', 'yellow', 'red']

    if sentiment == "Positive":
        heights = [1 + abs(polarity), 1 - abs(polarity), 0.5 - abs(polarity)]
    elif sentiment == "Negative":
        heights = [0.5 - abs(polarity), 1 - abs(polarity), 1 + abs(polarity)]
    else:
        heights = [0.5, 1, 0.5]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, heights, color=colors)
    plt.title("Sentiment Analysis Result")

    graph_path = os.path.join(GRAPH_FOLDER, file_name)
    plt.savefig(graph_path)
    plt.close()

    return graph_path


# ---------------- UI ----------------

st.title("📞 Sentiment Analysis of Helpdesk Calls")

uploaded_file = st.file_uploader("Upload Audio File", type=["wav"])

if uploaded_file is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            st.subheader("Transcription:")
            st.write(text)

            sentiment, emoji, polarity = get_sentiment(text)

            st.subheader("Sentiment Result:")
            st.write(f"{sentiment} {emoji}")

            graph_file = f"{uploaded_file.name}_graph.png"
            graph_path = plot_sentiment_graph(sentiment, polarity, graph_file)

            st.image(graph_path, caption="Sentiment Graph")

        except sr.UnknownValueError:
            st.error("Could not understand audio")

        except sr.RequestError:
            st.error("Speech recognition service unavailable")
