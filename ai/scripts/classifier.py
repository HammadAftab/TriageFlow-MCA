import joblib
from pathlib import Path
import math

BASE_DIR = Path(__file__).resolve().parent.parent

vectorizer = joblib.load(BASE_DIR / "models" / "tfidf_vectorizer.pkl")
classifier = joblib.load(BASE_DIR / "models" / "queue_classifier.pkl")


def predict_queue(subject, body):
    text = subject + " " + body

    X = vectorizer.transform([text])

    predicted_queue = classifier.predict(X)[0]

    # Confidence using decision_function
    #scores = classifier.decision_function(X)
    #confidence = float(scores.max())

    scores = classifier.decision_function(X)

    raw_score = float(scores.max())

    # Convert decision score to 0-1 confidence
    confidence = 1 / (1 + math.exp(-raw_score))

    return predicted_queue, confidence