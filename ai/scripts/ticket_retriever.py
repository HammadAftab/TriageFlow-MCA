from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

# Load Sentence Transformer model
#model = SentenceTransformer("all-MiniLM-L6-v2")
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)

# Load FAISS index
index = faiss.read_index(
    str(BASE_DIR / "models" / "faiss.index")
)

# Load ticket texts
with open(BASE_DIR / "models" / "ticket_texts.pkl", "rb") as f:
    ticket_texts = pickle.load(f)

# Load ticket resolutions
with open(BASE_DIR / "models" / "ticket_answers.pkl", "rb") as f:
    ticket_answers = pickle.load(f)


def retrieve_similar_tickets(subject, body, top_k=3):
    query = f"{subject.strip()} {body.strip()}"
    
    #embedding = model.encode([query], convert_to_numpy=True)
    embedding = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)

    distances, indices = index.search(embedding, top_k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        #results.append({
        #    "ticket": ticket_texts[idx].replace("\\n", "\n"),
        #    "resolution": ticket_answers[idx].replace("\\n", "\n"),
        #    "distance": float(distance)
        #})


        # FAISS returns cosine distance because the embeddings are normalized. 
        # So, converting it to cosine similarity.
        similarity = max(0.0, min(1.0, 1 - (float(distance) / 2)))

        results.append({
            "ticket": ticket_texts[idx].replace("\\n", "\n"),
            "resolution": ticket_answers[idx].replace("\\n", "\n"),
            "distance": float(distance),
            "similarity": similarity
        })

    return results