# Importing required libraries and models
import nltk
import pickle
import numpy as np
import json
import random
import logging
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from googletrans import Translator
from flask import Flask
from flask_socketio import SocketIO, emit
import os

# Setup
nltk.download('punkt')
nltk.download('wordnet')
lemma = WordNetLemmatizer()

# File existence check function
def load_file(filepath):
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"{filepath} not found.")
    return filepath

# Load model and data
model = load_model(load_file('model.h5'))
intents = json.loads(open(load_file('intents.json')).read())
words = pickle.load(open(load_file('word.pkl'), 'rb'))
classes = pickle.load(open(load_file('class.pkl'), 'rb'))

# Logging config
logging.basicConfig(level=logging.INFO)

# Preprocessing functions
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemma.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    cltn = np.zeros(len(words), dtype=np.float32)
    for word in sentence_words:
        for i, w in enumerate(words):
            if w == word:
                cltn[i] = 1
                if show_details:
                    logging.info(f"Found '{w}' in bag")
    return cltn

def predict_class(sentence, model):
    try:
        l = bow(sentence, words, show_details=False)
        res = model.predict(np.array([l]))[0]
    except Exception as e:
        logging.error(f"Error predicting class: {e}")
        return []  # Return empty list if prediction fails

    ERROR_THRESHOLD = 0.25
    results = [(i, j) for i, j in enumerate(res) if j > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)

    return_list = [{"intent": classes[k[0]], "probability": str(k[1])} for k in results]
    return return_list

def getResponse(ints, intents_json):
    if not ints:
        return "I'm not sure how to respond to that. Could you try asking something else?"
    tag = ints[0]['intent']
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])

# Translation support
def translate_message(message, source_language, target_language='en'):
    try:
        translator = Translator()
        translated_message = translator.translate(message, src=source_language, dest=target_language).text
        return translated_message
    except Exception as e:
        logging.error(f"Translation error: {e} | Source: {source_language} | Target: {target_language} | Message: {message}")
        return "Sorry, I couldn't translate your message."

# Main chatbot response function
def chatbotResponse(msg, source_language):
    translated_msg = translate_message(msg, source_language)
    ints = predict_class(translated_msg, model)
    res = getResponse(ints, intents)
    translated_response = translate_message(res, 'en', source_language)
    return translated_response

# Flask App and SocketIO setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.static_folder = 'static'
socketio = SocketIO(app, cors_allowed_origins="*")

# Basic test route to ensure the server is running
@app.route('/')
def home():
    return "Chatbot server is running!"

# SocketIO communication
@socketio.on('message')
def handle_message(data):
    try:
        source_language = data.get('language', 'en')
        user_message = data.get('message', '')
        if not user_message:
            emit('recv_message', "Please enter a message to get a response.")
            return

        response = chatbotResponse(user_message, source_language)
        logging.info(f"User: {user_message} | Bot: {response}")
        emit('recv_message', response)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        emit('recv_message', "Something went wrong. Please try again.")

# App entry point
if __name__ == "__main__":
    #  Render deployment compatibility update
    import eventlet
    eventlet.monkey_patch()
    socketio.run(app, host="0.0.0.0", port=5000)
