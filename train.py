import json
import pickle
import random
import nltk
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from preprocessing import clean_up_sentence

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')

# Load intents
try:
    with open('data/intents.json') as file:
        intents = json.load(file)
except FileNotFoundError:
    with open('../data/intents.json') as file:
        intents = json.load(file)

# Prepare training data
patterns = []
tags = []

for intent in intents['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])

# Encode labels
le = LabelEncoder()
y = le.fit_transform(tags)

# Build Pipeline: TF-IDF -> Logistic Regression
# We use our custom 'clean_up_sentence' from preprocessing.py as the tokenizer
pipe = Pipeline([
    ('vectorizer', TfidfVectorizer(tokenizer=clean_up_sentence, token_pattern=None)), 
    ('classifier', LogisticRegression(C=10, max_iter=1000))
])

# Train
print("Training model...")
pipe.fit(patterns, y)

# Save artifacts
print("Saving artifacts...")
with open('chatbot_model.pkl', 'wb') as f:
    pickle.dump(pipe, f)

with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)

print("✅ Model trained and saved successfully (Scikit-Learn)!")
