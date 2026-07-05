import os
import traceback
from dotenv import load_dotenv
from google import genai

load_dotenv()

key = os.getenv('GEMINI_API_KEY', '').strip()
print('key_present', bool(key))
client = genai.Client(api_key=key)

for model in ['gemini-1.5-flash', 'gemini-2.0-flash', 'gemini-2.0-flash-lite']:
    try:
        response = client.models.generate_content(model=model, contents='Say hello in one word')
        print('MODEL', model, 'OK')
        print('TEXT', getattr(response, 'text', None))
    except Exception as exc:
        print('MODEL', model, 'ERROR', repr(exc))
        traceback.print_exc()
