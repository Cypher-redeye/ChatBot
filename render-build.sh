#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Download NLTK data
python -m nltk.downloader punkt wordnet omw-1.4
python train.py
