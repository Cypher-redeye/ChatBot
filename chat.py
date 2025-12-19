import random
import os
import json
import pickle
import numpy as np
import tensorflow as tf
from preprocessing import bag_of_words

# ---------------- LOAD INTENTS ----------------
try:
    with open("data/intents.json") as file:
        intents = json.load(file)
        print("DEBUG: Loaded data/intents.json")
except FileNotFoundError:
    with open("../data/intents.json") as file:
        intents = json.load(file)
        print("DEBUG: Loaded ../data/intents.json")

# ---------------- LOAD MODEL & ARTIFACTS ----------------
MODEL_PATHS = [
    "chatbot_model.h5",
    "src/chatbot_model.h5"
]

model = None
words = None
classes = None

for path in MODEL_PATHS:
    if os.path.exists(path):
        base = os.path.dirname(path)
        words = pickle.load(open(os.path.join(base, "words.pkl"), "rb"))
        classes = pickle.load(open(os.path.join(base, "classes.pkl"), "rb"))
        model = tf.keras.models.load_model(path)
        print(f"DEBUG: Loaded model from {path}")
        break

if model is None:
    raise FileNotFoundError("❌ Model files not found!")

# ---------------- PREDICTION ----------------
def predict_class(sentence):
    bow = bag_of_words(sentence, words)

    # LSTM expects (batch, timesteps, features)
    bow = np.reshape(bow, (1, 1, len(bow)))

    predictions = model.predict(bow, verbose=0)[0]

    ERROR_THRESHOLD = 0.25
    results = [
        {"intent": classes[i], "probability": float(prob)}
        for i, prob in enumerate(predictions)
        if prob > ERROR_THRESHOLD
    ]

    results.sort(key=lambda x: x["probability"], reverse=True)
    return results

# ---------------- RESPONSE ----------------
def get_response(intents_list, intents_json):
    if not intents_list:
        return "Sorry, I didn't understand that."

    tag = intents_list[0]["intent"]

    for intent in intents_json["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Sorry, something went wrong."

# ---------------- CLI TEST ----------------
if __name__ == "__main__":
    print("🤖 Bot is running! (type 'quit' to exit)")

    while True:
        message = input("You: ")
        if message.lower() == "quit":
            break

        intents_list = predict_class(message)
        response = get_response(intents_list, intents)
        print("Bot:", response)
