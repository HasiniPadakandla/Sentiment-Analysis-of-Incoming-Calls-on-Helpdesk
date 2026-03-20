import streamlit as st
import speech_recognition as sr
import os
from sentiment import get_sentiment
import plotly.graph_objects as go

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Sentiment Analyzer", layout="wide")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- SIDEBAR ----------
st.sidebar.title("📌 About Project")
st.sidebar.info("""
AI-powered Helpdesk Sentiment Analyzer  
- Speech Recognition  
- NLP (VADER)  
- Graph-based Insights  
""")

# ---------- TITLE ----------
st.markdown("""
<h1 style='text-align: center; color: #4CAF50;'>
📞 Helpdesk Call Sentiment Analyzer
</h1>
""", unsafe_allow_html=True)

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("Upload Audio File", type=["wav"])

# ---------- GRAPH FUNCTIONS ----------
def plot_bar_graph(sentiment, polarity):
    labels = ['Positive', 'Neutral', 'Negative']

    values = [0.5, 1, 0.5]

    if sentiment == "Positive":
        values = [1 + abs(polarity), 1 - abs(polarity), 0.5]
    elif sentiment == "Negative":
        values = [0.5, 1 - abs(polarity), 1 + abs(polarity)]

    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker_color=['green', 'yellow', 'red']
        )
    ])

    fig.update_layout(
        title="📊 Sentiment Distribution",
        xaxis_title="Sentiment Type",
        yaxis_title="Score",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_pie_chart(sentiment, polarity):
    labels = ['Positive', 'Neutral', 'Negative']

    values = [0.5, 1, 0.5]

    if sentiment == "Positive":
        values = [1 + abs(polarity), 1 - abs(polarity), 0.5]
    elif sentiment == "Negative":
        values = [0.5, 1 - abs(polarity), 1 + abs(polarity)]

    fig = go.Figure(data=[
        go.Pie(labels=labels, values=values, hole=0.4)
    ])

    fig.update_layout(
        title="🥧 Sentiment Share",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)


# ---------- MAIN LOGIC ----------
if uploaded_file is not None:

    # 🔊 Show audio
    st.audio(uploaded_file, format="audio/wav")

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    recognizer = sr.Recognizer()

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
                col2.metric("Polarity Score", round(polarity, 2))
                col3.metric("Confidence", f"{abs(polarity)*100:.1f}%")

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

                # ---------- GRAPHS ----------
                st.subheader("📈 Sentiment Visualization")

                col1, col2 = st.columns(2)

                with col1:
                    plot_bar_graph(sentiment, polarity)

                with col2:
                    plot_pie_chart(sentiment, polarity)

                # ---------- DETAILS ----------
                with st.expander("🔍 View Detailed Info"):
                    st.write("Full Text:", text)
                    st.write("Polarity Score:", polarity)

            except sr.UnknownValueError:
                st.error("Could not understand audio")

            except sr.RequestError:
                st.error("Speech recognition service unavailable")
