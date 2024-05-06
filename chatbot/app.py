import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return " ".join(filtered_tokens)

conversations = [
    {"user": "Hello!", "bot": "Hi there! How can I help you today?"},
    {"user": "What's the weather like?", "bot": "I can't provide real-time weather information, but I can share some common phrases: Sunny, rainy, cloudy, windy, etc."},
    {"user": "I'm feeling bored. Do you have any suggestions?", "bot": "Sure! Here are a few ideas: Read a book, listen to music, watch a movie, learn a new skill, go for a walk, etc."},
    {"user": "Thank you!", "bot": "You're welcome! Is there anything else I can help you with?"},
]

def get_bot_response(user_message):
    preprocessed_message = preprocess_text(user_message)
    for conversation in conversations:
        if any(preprocessed_message in word for word in conversation["user"].split()):
            return conversation["bot"]
    return "I'm still under development, but I'm learning! How can I be of service?"

@app.route("/chat", methods=["GET"])
def chat_page():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    bot_response = get_bot_response(user_message)
    return jsonify({"message": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
