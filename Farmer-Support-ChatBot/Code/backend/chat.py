import warnings
warnings.filterwarnings("ignore")

import eventlet
eventlet.monkey_patch()

import os
import logging
import nltk
import pickle
import numpy as np
import json
import random
from nltk.stem import WordNetLemmatizer
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from googletrans import Translator

# Suppress noise
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Initialize
logging.basicConfig(level=logging.INFO, format='%(message)s')
lemma = WordNetLemmatizer()

# Load model and data
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('intents.json', 'r', encoding='utf-8') as f:
        intents = json.load(f)
    with open('word.pkl', 'rb') as f:
        words = pickle.load(f)
    with open('class.pkl', 'rb') as f:
        classes = pickle.load(f)
    logging.info(">>> Backend initialized successfully")
except Exception as e:
    logging.error(f">>> Failed to load model: {e}")
    model = None

# Chatbot Logic
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    return [lemma.lemmatize(word.lower()) for word in sentence_words]

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: bag[i] = 1
    return np.array(bag)

def predict_class(sentence, model):
    if model is None: return []
    p = bow(sentence, words)
    res = model.predict_proba(np.array([p]))[0]
    results = [[i,r] for i,r in enumerate(res) if r > 0.25]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]

def get_response(ints, intents_json):
    if not ints: return "I'm not sure how to respond to that."
    tag = ints[0]['intent']
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "I'm sorry, I don't understand."

# Server Setup
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return "Chatbot server is running."

@socketio.on('message')
def handle_message(data):
    lang = data.get('language', 'en')
    msg = data.get('message', '').strip()
    if not msg: return

    # Translation and Processing
    translator = Translator()
    try:
        eng_msg = translator.translate(msg, src=lang, dest='en').text if lang != 'en' else msg
        ints = predict_class(eng_msg, model)
        res = get_response(ints, intents)
        final_res = translator.translate(res, src='en', dest=lang).text if lang != 'en' else res
        
        logging.info(f"User ({lang}): {msg}")
        emit('recv_message', final_res)
    except Exception as e:
        logging.error(f"Error: {e}")
        emit('recv_message', "I'm having trouble translating that. Please try again.")

if __name__ == "__main__":
    logging.info(">>> Starting server on port 5000...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
