from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

vectorizer = joblib.load(BASE_DIR / "models" / "tfidf_vectorizer.pkl")
classifier = joblib.load(BASE_DIR / "models" / "queue_classifier.pkl")


def predict_queue(subject, body):
    text = f"{subject} {body}"

    X = vectorizer.transform([text])

    prediction = classifier.predict(X)[0]

    confidence = classifier.predict_proba(X).max()

    return prediction, float(confidence)