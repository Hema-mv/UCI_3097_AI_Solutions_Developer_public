from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

from scrapers.detector import detect_platform
from scrapers.walmart import scrape_walmart
from services.vector_store import store_reviews, search_reviews, collection_exists
from services.llm import generate_insight, ask_ollama

app = FastAPI(
    title="Review Intelligence V2 API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pydantic Models ───────────────────────────────────────
class ScrapeRequest(BaseModel):
    url: str
    max_reviews: int = 100

class InsightRequest(BaseModel):
    insight_type: str

# ── Routes ────────────────────────────────────────────────
@app.get("/health")
def health_check():
    return {"status": "ok", "version": "2.0.0"}


@app.post("/api/reviews/scrape")
def scrape_reviews(request: ScrapeRequest):
    try:
        # Detect platform
        platform = detect_platform(request.url)

        # Route to correct scraper
        if platform == "walmart":
            reviews = scrape_walmart(request.url, request.max_reviews)
        else:
            return {"status": "error", "message": f"Platform '{platform}' not supported yet. Coming soon!"}

        if not reviews:
            return {"status": "error", "message": "No reviews found for this product."}

        # Store in ChromaDB
        store_reviews(reviews)

        # Calculate stats
        avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
        high_rated = sum(1 for r in reviews if r["rating"] >= 4)

        return {
            "status": "success",
            "platform": platform,
            "review_count": len(reviews),
            "avg_rating": round(avg_rating, 2),
            "high_rated_pct": round(high_rated / len(reviews) * 100),
        }

    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": f"Scraping failed: {str(e)}"}


@app.post("/api/insights/generate")
def generate(request: InsightRequest):
    valid_types = ["summary", "complaints", "praises", "recommendations", "root_cause"]

    if request.insight_type not in valid_types:
        return {"status": "error", "message": f"Invalid type. Choose from {valid_types}"}

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