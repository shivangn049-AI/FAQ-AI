# FAQ Chatbot

A simple FAQ chatbot built with Flask and scikit-learn. It uses TF-IDF and cosine similarity to match user questions to a FAQ dataset.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open http://127.0.0.1:5000 in your browser.

## Project structure

- app.py: Flask routes and API
- chatbot/preprocessing.py: text cleaning, tokenization, stop-word removal, and lemmatization
- chatbot/matcher.py: TF-IDF matching engine
- chatbot/data/faqs.json: FAQ bank
- templates/index.html: chat UI
- static/css/style.css: styling
- static/js/script.js: frontend chat behavior
