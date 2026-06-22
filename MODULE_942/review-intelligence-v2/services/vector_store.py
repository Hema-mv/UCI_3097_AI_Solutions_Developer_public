import chromadb
import os
from services.embeddings import embed_texts

CHROMA_DIR = os.getenv("CHROMA_DIR", "./data/chroma_db")

client = chromadb.PersistentClient(path=CHROMA_DIR)

def store_reviews(reviews: list[dict], collection_name: str = "reviews") -> None:
    """Embed all reviews and store them in ChromaDB."""
    try:
        client.delete_collection(collection_name)
    except:
        pass

    collection = client.create_collection(collection_name)

    texts = [r["full_text"] for r in reviews]
    embeddings = embed_texts(texts)
    ids = [f"review_{i}" for i in range(len(reviews))]
    metadatas = [
        {"rating": r["rating"], "title": r["title"], "platform": r["platform"]}
        for r in reviews
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )
    print(f"Stored {len(reviews)} reviews in ChromaDB ✅")


def search_reviews(query: str, n_results: int = 10,
                   collection_name: str = "reviews") -> list[str]:
    """Find the most relevant reviews for a query."""
    collection = client.get_collection(collection_name)
    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results["documents"][0]


def collection_exists(collection_name: str = "reviews") -> bool:
    """Check if reviews have already been loaded."""
    try:
        client.get_collection(collection_name)
        return True
    except:
        return False