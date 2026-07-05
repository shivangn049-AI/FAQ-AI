import re
from typing import List

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
except Exception:  # pragma: no cover - fallback for minimal environments
    nltk = None
    stopwords = None
    WordNetLemmatizer = None
    word_tokenize = None


def _ensure_nltk_data() -> None:
    if nltk is None:
        return

    resources = ["punkt", "wordnet", "omw-1.4", "stopwords"]
    for resource in resources:
        try:
            if resource == "punkt":
                nltk.data.find("tokenizers/punkt")
            elif resource == "wordnet":
                nltk.data.find("corpora/wordnet")
            elif resource == "omw-1.4":
                nltk.data.find("corpora/omw-1.4")
            elif resource == "stopwords":
                nltk.data.find("corpora/stopwords")
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass


_ensure_nltk_data()

if WordNetLemmatizer is not None:
    lemmatizer = WordNetLemmatizer()
else:
    lemmatizer = None

if stopwords is not None:
    stop_words = set(stopwords.words("english"))
else:
    stop_words = set()


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokenize_text(text: str) -> List[str]:
    cleaned = clean_text(text)
    if not cleaned:
        return []
    if word_tokenize is not None:
        return word_tokenize(cleaned)
    return cleaned.split()


def remove_stopwords(tokens: List[str]) -> List[str]:
    return [token for token in tokens if token not in stop_words and len(token) > 1]


def lemmatize_tokens(tokens: List[str]) -> List[str]:
    if lemmatizer is None:
        return tokens
    return [lemmatizer.lemmatize(token) for token in tokens]


def preprocess_text(text: str) -> str:
    tokens = tokenize_text(text)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize_tokens(tokens)
    return " ".join(tokens)
