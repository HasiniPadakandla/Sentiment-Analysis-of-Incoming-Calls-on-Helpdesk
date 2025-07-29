from flask import Flask, request, render_template, jsonify, send_file
import speech_recognition as sr
import os
import matplotlib.pyplot as plt
from sentiment import get_sentiment  

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
GRAPH_FOLDER = "static/graphs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GRAPH_FOLDER'] = GRAPH_FOLDER

def plot_sentiment_graph(sentiment, polarity, file_name):
    labels = ['Positive', 'Neutral', 'Negative']
    colors = ['green', 'yellow', 'red']
    
    if sentiment == "Positive":
        heights = [1 + abs(polarity), 1 - abs(polarity), 0.5 - abs(polarity)]
    elif sentiment == "Negative":
        heights = [0.5 - abs(polarity), 1 - abs(polarity), 1 + abs(polarity)]
    else:  
        heights = [0.5, 1, 0.5]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, heights, color=colors)

    plt.xlabel('Sentiment')
    plt.ylabel('Score')
    plt.title('Sentiment Analysis Result')
    plt.ylim(0, max(heights) + 0.5)

    graph_path = os.path.join(app.config['GRAPH_FOLDER'], file_name)
    plt.savefig(graph_path)
    plt.close()
    return graph_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No file uploaded"})
    file = request.files['audio']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            
            sentiment, emoji, polarity = get_sentiment(text)

            graph_file_name = f"{file.filename.split('.')[0]}_sentiment.png"
            graph_path = plot_sentiment_graph(sentiment, polarity, graph_file_name)

            return jsonify({
                "transcription": text,
                "sentiment": sentiment,
                "emoji": emoji,
                "graph_url": f"/{graph_path}"
            })
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand audio"})
        except sr.RequestError:
            return jsonify({"error": "Speech recognition service unavailable"})

@app.route('/static/graphs/<filename>')
def get_graph(filename):
    return send_file(os.path.join(app.config['GRAPH_FOLDER'], filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
