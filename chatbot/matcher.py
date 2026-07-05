import json
import os
from typing import List, Dict, Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from chatbot.preprocessing import preprocess_text


class FAQMatcher:
    def __init__(self, faq_path: str):
        self.faq_path = faq_path
        self.faqs = self._load_faqs()
        self.questions = [item["question"] for item in self.faqs]
        self.answers = [item["answer"] for item in self.faqs]
        self.categories = [item.get("category", "general") for item in self.faqs]

        if self.questions:
            self.vectorizer = TfidfVectorizer()
            self.matrix = self.vectorizer.fit_transform(self.questions)
        else:
            self.vectorizer = TfidfVectorizer()
            self.matrix = None

    def _load_faqs(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.faq_path):
            return []
        with open(self.faq_path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def get_answer(self, user_query: str) -> Dict[str, Any]:
        processed_query = preprocess_text(user_query)
        if not processed_query:
            return {
                "reply": "Please ask a clearer question so I can help you.",
                "confidence": 0.0,
                "category": "general",
            }

        if self.matrix is None:
            return {
                "reply": "I do not have FAQ data available yet.",
                "confidence": 0.0,
                "category": "general",
            }

        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.matrix).flatten()
        best_index = int(similarities.argmax())
        best_score = float(similarities[best_index])

        if best_score < 0.2:
            return {
                "reply": "I could not find a strong match. Please ask a related question or contact support.",
                "confidence": round(best_score, 2),
                "category": "general",
            }

        return {
            "reply": self.answers[best_index],
            "confidence": round(best_score, 2),
            "category": self.categories[best_index],
        }
