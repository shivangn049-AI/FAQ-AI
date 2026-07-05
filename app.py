import os

import requests
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

from chatbot.matcher import FAQMatcher

load_dotenv()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

faq_path = os.path.join(os.path.dirname(__file__), "chatbot", "data", "faqs.json")
matcher = FAQMatcher(faq_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()


def get_gemini_reply(message: str):
    if not GEMINI_API_KEY:
        print("Gemini API key is missing")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "You are a helpful support assistant for a website. "
                            "Answer briefly, clearly, and politely.\n\n"
                            f"User question: {message}"
                        )
                    }
                ],
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        print("Gemini status:", response.status_code)
        print("Gemini response body:", response.text)
        if response.status_code != 200:
            return None

        data = response.json()
        candidates = data.get("candidates", [])
        for candidate in candidates:
            content = candidate.get("content", {})
            parts = content.get("parts", [])
            for part in parts:
                text = part.get("text", "")
                if text:
                    return text.strip()
    except Exception as exc:
        print("Gemini request exception:", repr(exc))
        return None

    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "Please enter a question so I can help you.", "confidence": 0.0, "category": "general"})

    fallback_response = matcher.get_answer(message)

    if GEMINI_API_KEY:
        gemini_reply = get_gemini_reply(message)
        if gemini_reply:
            return jsonify({"reply": gemini_reply, "confidence": 0.95, "category": "ai"})

    if fallback_response.get("confidence", 0.0) < 0.2:
        return jsonify({
            "reply": (
                "I couldn't find a strong match in the FAQ list. "
                "You can try a more specific question, or contact support@example.com for help."
            ),
            "confidence": round(fallback_response.get("confidence", 0.0), 2),
            "category": "general",
        })

    return jsonify(fallback_response)


if __name__ == "__main__":
    app.run(debug=True)
