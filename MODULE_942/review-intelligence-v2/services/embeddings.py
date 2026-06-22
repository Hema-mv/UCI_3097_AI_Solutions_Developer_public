from sentence_transformers import SentenceTransformer

# Load the model once when this file is imported
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert a list of text strings into embedding vectors.
    """
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings.tolist()