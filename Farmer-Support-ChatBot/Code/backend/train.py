""" This file is used to train the model and save it as model.pkl file. """

# Importing the required libraries
import nltk
import json
import pickle
import numpy as np
from sklearn.neural_network import MLPClassifier
import random
from nltk.stem import WordNetLemmatizer

# Ensure NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

lemma = WordNetLemmatizer()

# Preprocessing the data
words = []
classes = []
docs = []
ignore_words = ['?', '!', '', "'"]
data_file = open('intents.json', encoding='utf-8').read()
intents = json.loads(data_file)

# Tokenizing the words
for i in intents['intents']:
    for pattern in i['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        docs.append((w, i['tag']))

        if i['tag'] not in classes:
            classes.append(i['tag'])

# Lemmatizing the words
words = [lemma.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# Sorting the classes
classes = sorted(list(set(classes)))

# Printing the length of the documents, classes and words
print(len(docs), "documents")
print(len(classes), "classes", classes)
print(len(words), "unique lemmatized words")

# Saving the words and classes in pickle files
with open('word.pkl', 'wb') as f:
    pickle.dump(words, f)
with open('class.pkl', 'wb') as f:
    pickle.dump(classes, f)

# Creating the training data
training = []
output_empty = [0] * len(classes)

# Creating the bag of words
for d in docs:
    bag = []
    pattern_words = d[0]
    pattern_words = [lemma.lemmatize(word.lower()) for word in pattern_words]
    
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # Scikit-learn supports 1D label targets directly, but since we want probabilities,
    # and the original logic used one-hot encoding, we'll keep the one-hot structure
    # which MLPClassifier also natively supports.
    output_row = list(output_empty)
    output_row[classes.index(d[1])] = 1
    
    training.append([bag, output_row])

# Shuffling the training data
random.shuffle(training)

x_train = [row[0] for row in training]
y_train = [row[1] for row in training]
print("Created Training data Successfully")

# Creating the model : Scikit-learn MLP Classifier (same architecture as before)
model = MLPClassifier(
    hidden_layer_sizes=(150, 150),
    activation='relu',
    solver='sgd',
    learning_rate_init=0.01,
    momentum=0.9,
    nesterovs_momentum=True,
    max_iter=250,
    batch_size=5,
    verbose=True
)

# Fitting the model
print("Training the model...")
model.fit(np.array(x_train), np.array(y_train))

# Save the trained scikit-learn model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Successful model creation and saved as model.pkl")

# Evaluating the model
accuracy = model.score(np.array(x_train), np.array(y_train))
print(f'Training Accuracy: {accuracy * 100:.2f}%')