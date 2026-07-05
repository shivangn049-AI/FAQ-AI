import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('GEMINI_API_KEY', '').strip()
print('KEY_PRESENT', bool(key))

for model in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-2.0-flash-lite']:
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}'
    payload = {'contents': [{'parts': [{'text': 'Say hello in one word'}]}]}
    try:
        r = requests.post(url, json=payload, timeout=60)
        print('MODEL', model, 'STATUS', r.status_code)
        print(r.text[:1000])
    except Exception as exc:
        print('MODEL', model, 'ERROR', repr(exc))
