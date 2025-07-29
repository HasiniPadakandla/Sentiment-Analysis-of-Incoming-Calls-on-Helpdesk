import os
import speech_recognition as sr
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score

# Define file paths
audio_files = ["/mnt/data/28.wav", "/mnt/data/242.wav"]
actual_labels = ["Positive", "Negative"]  # Expected sentiments for evaluation

# Speech-to-text and sentiment analysis
def get_transcription_and_sentiment(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            analyzer = SentimentIntensityAnalyzer()
            score = analyzer.polarity_scores(text)
            
            if score['compound'] >= 0.05:
                return "Positive", text
            elif score['compound'] <= -0.05:
                return "Negative", text
            else:
                return "Neutral", text
        except Exception as e:
            return "Error", ""

# Evaluate Sentiments
predicted_labels = []
transcriptions = []

for file in audio_files:
    sentiment, transcription = get_transcription_and_sentiment(file)
    if sentiment != "Error":
        predicted_labels.append(sentiment)
        transcriptions.append(transcription)

# Evaluate Model Performance
if len(predicted_labels) == len(actual_labels):
    accuracy = accuracy_score(actual_labels, predicted_labels)

    # Confusion Matrix
    conf_matrix = confusion_matrix(actual_labels, predicted_labels, labels=["Positive", "Neutral", "Negative"])
    
    # Plot Confusion Matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Positive", "Neutral", "Negative"],
                yticklabels=["Positive", "Neutral", "Negative"])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    conf_matrix_path = "/mnt/data/confusion_matrix.png"
    plt.savefig(conf_matrix_path)
    plt.close()

    # Prepare results
    result_summary = {
        "transcriptions": transcriptions,
        "predicted_labels": predicted_labels,
        "actual_labels": actual_labels,
        "accuracy": accuracy * 100,
        "conf_matrix_path": conf_matrix_path
    }
else:
    result_summary = {"error": "Mismatch in actual and predicted label counts."}

result_summary
