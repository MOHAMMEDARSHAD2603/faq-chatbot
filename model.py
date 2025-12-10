import json
import re
from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure NLTK resources are available
def ensure_nltk_resources():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")

    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet")

ensure_nltk_resources()

STOPWORDS = set(stopwords.words("english"))
LEMMA = WordNetLemmatizer()

def load_faqs(path: str = "faqs.json") -> List[Dict[str, str]]:
    """Load FAQs from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        faqs = json.load(f)
    if not faqs:
        raise ValueError("FAQ list is empty. Please check faqs.json")
    return faqs

def normalize(text: str) -> str:
    """Normalize text for better matching."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    tokens = [LEMMA.lemmatize(t) for t in tokens]
    return " ".join(tokens)

class FAQMatcher:
    def __init__(self, faqs: List[Dict[str, str]]):
        self.faqs = faqs
        self.questions = [faq["question"] for faq in faqs]
        self.answers = [faq["answer"] for faq in faqs]
        self.categories = [faq.get("category", "General") for faq in faqs]
        self.norm_questions = [normalize(q) for q in self.questions]

        # TF-IDF vectorizer with unigrams + bigrams
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(self.norm_questions)

    def best_match(self, user_question: str) -> Tuple[str, str, str, float]:
        """Return best matching question, answer, category, and score."""
        nq = normalize(user_question)
        vec = self.vectorizer.transform([nq])
        sims = cosine_similarity(vec, self.matrix)[0]
        idx = int(np.argmax(sims))
        score = float(sims[idx])
        return self.questions[idx], self.answers[idx], self.categories[idx], score