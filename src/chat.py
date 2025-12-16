import random
import os
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer
from preprocessing import clean_up_sentence, bag_of_words

lemmatizer = WordNetLemmatizer()

# Load artifacts
try:
    with open('../data/intents.json') as file:
        intents = json.load(file)
except FileNotFoundError:
    with open('data/intents.json') as file:
        intents = json.load(file)

# Load model and pickles
# Check current directory then src directory
if os.path.exists('chatbot_model.h5'):
    words = pickle.load(open('words.pkl', 'rb'))
    classes = pickle.load(open('classes.pkl', 'rb'))
    model = tf.keras.models.load_model('chatbot_model.h5')
elif os.path.exists('src/chatbot_model.h5'):
    words = pickle.load(open('src/words.pkl', 'rb'))
    classes = pickle.load(open('src/classes.pkl', 'rb'))
    model = tf.keras.models.load_model('src/chatbot_model.h5')
else:
    # Fallback to absolute assumption or error
    print("Error: Could not find model files.")
    exit()



def predict_class(sentence):
    bow = bag_of_words(sentence, words)
    # Reshape for LSTM: (1, 1, features)
    res = model.predict(np.array([bow]).reshape(1, 1, len(bow)))[0]
    
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("GO! Bot is running! (type 'quit' to exit)")

while True:
    message = input("")
    if message.lower() == "quit":
        break
    
    ints = predict_class(message)
    if ints:
        res = get_response(ints, intents)
        print(res)
    else:
        print("I didn't understand that.")
