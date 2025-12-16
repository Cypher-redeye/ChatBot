# AI Customer Support Chatbot

An intelligent chatbot built with Python, TensorFlow (LSTM), and NLTK. It classifies user intents (like "greeting", "hours", "options") to provide automated customer support responses.

## Features
- **Natural Language Understanding**: Uses NLTK for tokenization and lemmatization.
- **Deep Learning Model**: A Long Short-Term Memory (LSTM) neural network trained with TensorFlow/Keras.
- **Customizable**: Easy to extend with new intents in `data/intents.json`.

## Installation

1. **Clone the repository** (if moving to a new machine):
   ```bash
   git clone <your-repo-url>
   cd ChatBot
   ```

2. **Create and activate a virtual environment** (Recommended Python 3.10):
   ```bash
   # Windows
   py -3.10 -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Install dependencies**:
   ```bash
   pip install tensorflow nltk numpy colorama
   ```

## Usage

### Running the Chatbot
To start the chat interface:
```bash
python src/chat.py
```

### Retraining the Model
If you add new patterns to `data/intents.json`, you must retrain the model:
```bash
python src/train.py
```
This generates new `chatbot_model.h5`, `words.pkl`, and `classes.pkl` files.

## Project Structure
- `data/intents.json`: Training data (patterns and responses).
- `src/preprocessing.py`: Text cleaning utilities.
- `src/train.py`: Model training script.
- `src/chat.py`: Inference script for the chat interface.
