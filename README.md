# 📞 Sentiment Analysis of Incoming Calls on Helpdesk

### Live URL : https://sentiment-analysis-of-incoming-calls.streamlit.app/

### Demo of Sentiment Analyzer: 
https://github.com/user-attachments/assets/3d6d7dcb-b7e6-432c-a91e-23808863f633

## 🚀 Overview

This project is an AI-powered application that analyzes customer support calls and determines the **sentiment of the conversation**. It converts audio into text using speech recognition and applies NLP techniques to classify sentiment as **Positive, Negative, or Neutral**.

The system also provides **visual insights** using interactive graphs, making it useful for monitoring customer satisfaction in helpdesk environments.

---

## 🎯 Key Features

* 🎧 Upload audio files (WAV format)
* 📝 Automatic speech-to-text transcription
* 😊 Sentiment classification (Positive / Neutral / Negative)
* 📊 Sentiment visualization:

  * Bar Graph (distribution)
  * Pie Chart (proportion)
* 📈 Polarity score with confidence level
* 💡 Clean and interactive Streamlit UI

---

## 🛠️ Tech Stack

| Category           | Tools / Libraries           |
| ------------------ | --------------------------- |
| Language           | Python                      |
| Frontend           | Streamlit                   |
| NLP                | VADER Sentiment Analysis    |
| Speech Recognition | Google Speech API           |
| Visualization      | Plotly                      |
| ML Libraries       | Scikit-learn, Numpy, Pandas |

---

## 🧠 How It Works

1. User uploads an audio file
2. Audio is converted to text using speech recognition
3. Text is analyzed using VADER sentiment analyzer
4. Sentiment and polarity score are calculated
5. Results are displayed using graphs and metrics

---

## 📊 Output Example

* **Transcription:**
  "The service was really helpful and quick."

* **Sentiment:** Positive 😊

* **Polarity Score:** 0.82

* **Confidence:** 82%

* **Visualizations:**

  * 📊 Bar graph (sentiment distribution)
  * 🥧 Pie chart (sentiment share)

---

## 📁 Project Structure

```
Sentiment-Analysis-of-Incoming-Calls-on-Helpdesk/
│
├── app.py                  # Main Streamlit application
├── sentiment.py           # Sentiment analysis logic (VADER)
├── requirements.txt       # Dependencies
├── uploads/               # Uploaded audio files
└── README.md              # Project documentation
```

---

## ⚙️ Installation & Setup

### 🔹 Clone the Repository

```
git clone https://github.com/HasiniPadakandla/Sentiment-Analysis-of-Incoming-Calls-on-Helpdesk.git
cd Sentiment-Analysis-of-Incoming-Calls-on-Helpdesk
```

### 🔹 Install Dependencies

```
pip install -r requirements.txt
```

### 🔹 Run the Application

```
streamlit run app.py
```

---

## 🌐 Deployment

This project is deployed using **Streamlit Cloud**.

👉 You can deploy by connecting your GitHub repository to Streamlit Cloud and selecting `app.py` as the main file.

---

## ⚠️ Limitations

* Supports only WAV audio format
* Requires clear audio for accurate transcription
* Microphone input is not supported in cloud deployment

---

## 🔮 Future Enhancements

* 🎙️ Real-time call sentiment tracking
* 📊 Multi-call comparison dashboard
* 🤖 AI-based response suggestions for agents
* 🌍 Multi-language support

---

## 👩‍💻 Author

**Hasini Padakandla**

* 💼 Aspiring AI/ML Developer
* 🔗 GitHub: https://github.com/HasiniPadakandla

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share your feedback!
