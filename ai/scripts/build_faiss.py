import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss

from pathlib import Path
import pickle


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET = BASE_DIR / "datasets" / "processed" / "resolved_tickets.csv"

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_csv(DATASET)

texts = df["query_text"].astype(str).tolist()
answers = df["answer"].astype(str).tolist()

print("Generating embeddings...")

embeddings = MODEL.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(
    index,
    str(BASE_DIR / "models" / "faiss.index")
)

with open(BASE_DIR / "models" / "ticket_answers.pkl", "wb") as f:
    pickle.dump(answers, f)

with open(BASE_DIR / "models" / "ticket_texts.pkl", "wb") as f:
    pickle.dump(texts, f)

print()
print("Finished")
print("Vectors :", index.ntotal)
print("Dimension :", dimension)