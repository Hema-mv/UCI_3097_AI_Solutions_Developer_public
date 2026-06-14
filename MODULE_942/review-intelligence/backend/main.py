from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.loader import load_reviews
from services.vector_store import store_reviews, search_reviews, collection_exists
from services.llm import generate_insight

app = FastAPI(
    title="Review Intelligence API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pydantic Models ───────────────────────────────────────
class LoadRequest(BaseModel):
    csv_path: str = "data/reviews.csv"
    max_rows: int = 300

class InsightRequest(BaseModel):
    insight_type: str

# ── Routes ────────────────────────────────────────────────
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/reviews/load")
def load(request: LoadRequest):
    reviews = load_reviews(request.csv_path, request.max_rows)
    store_reviews(reviews)
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
    return {
        "status": "success",
        "review_count": len(reviews),
        "avg_rating": round(avg_rating, 2)
    }


@app.post("/api/insights/generate")
def generate(request: InsightRequest):
    valid_types = ["summary", "complaints", "praises", "recommendations", "root_cause"]
    if request.insight_type not in valid_types:
        return {"error": f"Invalid type. Choose from {valid_types}"}

    search_queries = {
        "summary":         "overall product experience quality",
        "complaints":      "problem issue broken disappointed negative bad",
        "praises":         "love great excellent amazing perfect best",
        "recommendations": "wish improve suggest better feature want",
        "root_cause":      "why broke stopped working failed issue reason",
    }

    query = search_queries[request.insight_type]
    relevant_reviews = search_reviews(query, n_results=15)
    result = generate_insight(request.insight_type, relevant_reviews)

    return {
        "insight_type": request.insight_type,
        "content": result,
        "supporting_reviews": relevant_reviews[:3]
    }


@app.get("/api/reviews/status")
def status():
    return {"reviews_loaded": collection_exists()}