# 🛠️ Implementation Guide: AI Multi Marketplace Customer Review Intelligence System
## Version 2 — Live Scraping Edition

> **Student:** Hemalatha Mohan | **Program:** Per Scholas CAP 942 | **Project:** UCI_3097 AI Solutions Developer
> 
> This guide reflects the **actual code built** in Version 2. Use it as your reference for documentation, presentation, and future development.

---

## 📁 Project Structure

```
review-intelligence-v2/
├── pyproject.toml              # UV project config + dependencies
├── .env                        # API keys / config (never commit!)
├── .gitignore
├── RUN_GUIDE_V2.md             # How to run the project
├── README.md                   # GitHub documentation
│
├── backend/
│   ├── __init__.py
│   └── main.py                 # FastAPI app — all routes in one file
│
├── scrapers/
│   ├── __init__.py
│   ├── detector.py             # Detects platform from URL
│   ├── walmart.py              # Walmart scraper via RapidAPI ✅
│   ├── etsy.py                 # Etsy scraper via Official API ⏳
│   └── amazon.py               # Amazon scraper via RapidAPI 🔜
│
├── services/
│   ├── __init__.py
│   ├── embeddings.py           # SentenceTransformers
│   ├── vector_store.py         # ChromaDB store + search
│   └── llm.py                  # Ollama + RAG prompts
│
├── data/
│   └── chroma_db/              # Auto-created vector database
│
├── test_walmart.py             # Walmart scraper test
└── test_etsy.py                # Etsy scraper test
```

---

## ⚙️ Phase 0: Project Setup

### Step 0.1 — Install UV

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:
```powershell
uv --version
```

### Step 0.2 — Create project with Python 3.11

```powershell
mkdir review-intelligence-v2
cd review-intelligence-v2
uv init --python 3.11
uv venv --python 3.11
.venv\Scripts\activate
```

### Step 0.3 — Install all dependencies

```powershell
uv add fastapi uvicorn streamlit sentence-transformers chromadb pandas python-dotenv httpx spacy playwright
```

### Step 0.4 — Install additional tools

```powershell
uv run playwright install chromium
uv run python -m spacy download en_core_web_sm
```

### Step 0.5 — Install Ollama and pull Mistral

1. Download from `https://ollama.com`
2. Install like a normal Windows app
3. Pull the model:

```powershell
ollama pull mistral
```

Test it:
```powershell
ollama run mistral "Say hello in one sentence."
```

### Step 0.6 — Create your `.env` file

```
RAPIDAPI_KEY=your_rapidapi_key_here
RAPIDAPI_HOST=real-time-walmart-data1.p.rapidapi.com
ETSY_API_KEY=your_etsy_api_key_here
LLM_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
CHROMA_DIR=./data/chroma_db
```

### Step 0.7 — Create `.gitignore`

```
.env
.venv/
data/chroma_db/
__pycache__/
*.pyc
```

### Step 0.8 — Create folder structure

```powershell
mkdir scrapers
mkdir services
mkdir backend
mkdir data
New-Item scrapers\__init__.py -type file
New-Item scrapers\detector.py -type file
New-Item scrapers\walmart.py -type file
New-Item scrapers\etsy.py -type file
New-Item scrapers\amazon.py -type file
New-Item services\__init__.py -type file
New-Item services\embeddings.py -type file
New-Item services\vector_store.py -type file
New-Item services\llm.py -type file
New-Item backend\__init__.py -type file
New-Item backend\main.py -type file
New-Item app.py -type file
```

---

## 🔍 Phase 1: Platform Detection

**File:** `scrapers/detector.py`

```python
from urllib.parse import urlparse

def detect_platform(url: str) -> str:
    """Detect which marketplace the URL belongs to."""
    domain = urlparse(url).netloc.lower()

    if "walmart.com" in domain:
        return "walmart"
    elif "etsy.com" in domain:
        return "etsy"
    elif "amazon.com" in domain or "amazon.in" in domain:
        return "amazon"
    else:
        raise ValueError(f"Unsupported platform. Please use Walmart, Etsy, or Amazon URLs.")


def extract_walmart_id(url: str) -> str:
    """Extract the item ID from a Walmart URL."""
    path = urlparse(url).path
    parts = path.strip("/").split("/")
    for part in reversed(parts):
        if part.isdigit():
            return part
    raise ValueError("Could not find Walmart item ID in URL.")
```

> **How it works:** Reads the domain from the URL and returns the platform name. Each scraper then uses the platform-specific ID extractor to pull the product ID.

---

## 🛒 Phase 2: Platform Scrapers

### Step 2.1 — Walmart Scraper (✅ Complete)

**Why RapidAPI:** Walmart uses GraphQL + PerimeterX bot detection. Direct scraping is blocked. RapidAPI acts as a middleware that handles all the bot bypass.

**API Used:** Real-Time Walmart Data by OpenWeb Ninja
- **Host:** `real-time-walmart-data1.p.rapidapi.com`
- **Endpoint:** `GET /product-reviews`
- **Parameters:** `product_id`, `page`, `domain=us`, `limit=10`
- **Free tier:** $0/month (BASIC plan)

**File:** `scrapers/walmart.py`

```python
import httpx
import os
import time
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY  = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "Content-Type": "application/json",
    "x-rapidapi-host": RAPIDAPI_HOST,
    "x-rapidapi-key": RAPIDAPI_KEY,
}

def scrape_walmart(url: str, max_reviews: int = 100) -> list[dict]:
    """
    Fetch Walmart reviews using RapidAPI Real-Time Walmart Data.
    User pastes a Walmart URL — everything else is automatic.
    """
    from scrapers.detector import extract_walmart_id
    item_id = extract_walmart_id(url)
    print(f"Fetching reviews for Walmart item: {item_id}")

    reviews = []
    page = 1

    while len(reviews) < max_reviews:
        params = {
            "product_id": item_id,
            "page": str(page),
            "domain": "us",
            "limit": "10",
            "sort": "relevancy"
        }

        try:
            response = httpx.get(
                "https://real-time-walmart-data1.p.rapidapi.com/product-reviews",
                headers=HEADERS,
                params=params,
                timeout=30.0
            )

            if response.status_code != 200:
                print(f"API error: {response.status_code}")
                break

            data = response.json()
            page_reviews = data.get("data", {}).get("reviews", [])

            if not page_reviews:
                print(f"No more reviews at page {page}")
                break

            for r in page_reviews:
                rating = r.get("rating", 3)
                title  = r.get("title", "")
                body   = r.get("reviewText", "") or r.get("text", "") or r.get("body", "")

                if body:
                    reviews.append({
                        "platform": "walmart",
                        "rating": float(rating),
                        "title": str(title),
                        "body": str(body),
                        "full_text": f"{title}. {body}",
                    })

            print(f"Page {page}: got {len(page_reviews)} reviews (total: {len(reviews)})")
            page += 1
            time.sleep(0.5)

        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    print(f"Total reviews fetched: {len(reviews)}")
    return reviews[:max_reviews]
```

**Test it:**
```python
# test_walmart.py
from scrapers.walmart import scrape_walmart

url = "https://www.walmart.com/ip/Neutrogena-Hydro-Boost-Water-Gel-Face-Moisturizer-Lotion-with-Hyaluronic-Acid-1-7-oz/40488263"
reviews = scrape_walmart(url, max_reviews=30)
print(f"Total: {len(reviews)}")
for r in reviews[:3]:
    print(f"Rating: {r['rating']} | {r['body'][:100]}")
```

```powershell
uv run python test_walmart.py
```

> ✅ **Expected output:** 30 reviews fetched across 3 pages with real review text.

---

### Step 2.2 — Etsy Scraper (⏳ Pending API Approval)

**Why Official Etsy API:** Etsy blocks Playwright with CAPTCHA verification. RapidAPI free tiers are too limited (5 requests/month). The official Etsy API is free with 5,000 requests/day.

**How to get your API key:**
1. Go to `https://www.etsy.com/developers`
2. Click "Create a New App"
3. Fill in app details
4. Wait for approval (1-2 days)

**API Details:**
- **Endpoint:** `GET https://openapi.etsy.com/v3/application/listings/{listing_id}/reviews`
- **Header:** `x-api-key: YOUR_ETSY_KEY`
- **Free tier:** 5,000 requests/day

**File:** `scrapers/etsy.py`

```python
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

ETSY_API_KEY = os.getenv("ETSY_API_KEY")

def extract_etsy_id(url: str) -> str:
    """Extract listing ID from Etsy URL."""
    # Etsy URLs: https://www.etsy.com/listing/1654494480/product-name
    parts = url.split("/listing/")
    if len(parts) > 1:
        return parts[1].split("/")[0].split("?")[0]
    raise ValueError("Could not find Etsy listing ID in URL")


def scrape_etsy(url: str, max_reviews: int = 100) -> list[dict]:
    """
    Fetch Etsy reviews using the official Etsy Open API v3.
    Requires a free API key from https://www.etsy.com/developers
    """
    listing_id = extract_etsy_id(url)
    print(f"Etsy listing ID: {listing_id}")

    reviews = []
    offset = 0
    limit = 25

    headers = {"x-api-key": ETSY_API_KEY}

    while len(reviews) < max_reviews:
        try:
            response = httpx.get(
                f"https://openapi.etsy.com/v3/application/listings/{listing_id}/reviews",
                headers=headers,
                params={"limit": limit, "offset": offset},
                timeout=30.0
            )

            if response.status_code != 200:
                print(f"API error: {response.status_code} — {response.text[:200]}")
                break

            data = response.json()
            results = data.get("results", [])

            if not results:
                print(f"No more reviews at offset {offset}")
                break

            for r in results:
                body = r.get("review", "") or ""
                rating = r.get("rating", 3)

                if body:
                    reviews.append({
                        "platform": "etsy",
                        "rating": float(rating),
                        "title": "",
                        "body": body,
                        "full_text": body,
                    })

            print(f"Offset {offset}: got {len(results)} reviews (total: {len(reviews)})")
            offset += limit

        except Exception as e:
            print(f"Error at offset {offset}: {e}")
            break

    print(f"Total Etsy reviews: {len(reviews)}")
    return reviews[:max_reviews]
```

**Test it (after API key is approved):**
```python
# test_etsy.py
from scrapers.etsy import scrape_etsy

url = "https://www.etsy.com/listing/1797455914/gold-plated-enamel-sakura-flower"
reviews = scrape_etsy(url, max_reviews=50)
print(f"Total: {len(reviews)}")
for r in reviews[:3]:
    print(f"Rating: {r['rating']} | {r['body'][:100]}")
```

---

### Step 2.3 — Amazon Scraper (🔜 Next)

**Why RapidAPI:** Amazon has the strongest bot detection of all platforms (Cloudflare + fingerprinting). Direct scraping is practically impossible. RapidAPI handles it.

**API to use:** Search RapidAPI for "Real-Time Amazon Data" or "Amazon Product Reviews"

**File:** `scrapers/amazon.py` — to be built

```python
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def extract_amazon_asin(url: str) -> str:
    """
    Extract ASIN from Amazon URL.
    ASINs are 10-character alphanumeric strings.
    Example: https://www.amazon.com/dp/B08N5WRWNW → B08N5WRWNW
    """
    # TODO: Extract ASIN from URL
    # Hint: Look for /dp/ASIN or /product/ASIN in the path
    pass


def scrape_amazon(url: str, max_reviews: int = 100) -> list[dict]:
    """
    Fetch Amazon reviews using RapidAPI.
    """
    asin = extract_amazon_asin(url)
    print(f"Amazon ASIN: {asin}")

    reviews = []

    # TODO: Call RapidAPI Amazon reviews endpoint
    # Similar pattern to Walmart scraper

    return reviews[:max_reviews]
```

---

## 🔢 Phase 3: Embeddings

**File:** `services/embeddings.py`

```python
from sentence_transformers import SentenceTransformer

# Load the model once — saves time on repeated calls
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert a list of text strings into 384-dimensional embedding vectors.
    Similar meanings → similar vectors → ChromaDB finds them together.
    """
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings.tolist()
```

> **Why MiniLM:** Small (90MB), fast, and produces high-quality embeddings for semantic search. Perfect for running locally without a GPU.

---

## 🗄️ Phase 4: ChromaDB Vector Store

**File:** `services/vector_store.py`

```python
import chromadb
import os
from services.embeddings import embed_texts

CHROMA_DIR = os.getenv("CHROMA_DIR", "./data/chroma_db")
client = chromadb.PersistentClient(path=CHROMA_DIR)

def store_reviews(reviews: list[dict], collection_name: str = "reviews") -> None:
    """Embed all reviews and store in ChromaDB. Replaces existing data."""
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
    """Semantic search — finds reviews by meaning, not just keywords."""
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
```

---

## 🤖 Phase 5: LLM + RAG Pipeline

**File:** `services/llm.py`

```python
import httpx
import os

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("LLM_MODEL", "mistral")

SYSTEM_PROMPT = """You are a product review analyst helping e-commerce sellers
understand their customer feedback. Be specific, concise, and always base your
analysis only on the reviews provided. Use bullet points where helpful."""


def ask_ollama(prompt: str) -> str:
    """Send a prompt to Ollama and return the text response."""
    try:
        response = httpx.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "system": SYSTEM_PROMPT,
                "stream": False
            },
            timeout=120.0
        )
        response.raise_for_status()
        return response.json()["response"]
    except httpx.ConnectError:
        return "❌ Could not connect to Ollama. Make sure it is running."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def build_prompt(insight_type: str, context_reviews: list[str]) -> str:
    """RAG step: build a structured prompt with retrieved reviews as context."""
    context = "\n\n".join([f"- {r[:300]}" for r in context_reviews])

    prompts = {
        "summary": f"""Based on these customer reviews, write a 3-paragraph summary:
Paragraph 1: Overall customer sentiment
Paragraph 2: What customers love most
Paragraph 3: Main areas of concern

CUSTOMER REVIEWS:
{context}

SUMMARY:""",

        "complaints": f"""List the TOP 5 most common complaints from these reviews.
For each complaint:
• State the issue in one sentence
• Give one short example from the reviews

CUSTOMER REVIEWS:
{context}

TOP COMPLAINTS:""",

        "praises": f"""List the TOP 5 things customers praise most from these reviews.
For each praise:
• State what they love in one sentence
• Give one short example from the reviews

CUSTOMER REVIEWS:
{context}

TOP PRAISES:""",

        "recommendations": f"""Based on these customer reviews, suggest 5 specific
product improvements the seller should make.
For each: explain what to fix and why customers want it.

CUSTOMER REVIEWS:
{context}

RECOMMENDATIONS:""",

        "root_cause": f"""Analyze these reviews and identify the ROOT CAUSES of the
main problems customers experience. Go beyond the surface complaint to explain
WHY the problem happens.

CUSTOMER REVIEWS:
{context}

ROOT CAUSE ANALYSIS:""",
    }

    return prompts.get(insight_type, f"Analyze these reviews:\n\n{context}")


def generate_insight(insight_type: str, context_reviews: list[str]) -> str:
    """Full RAG pipeline: build prompt → call Ollama → return result."""
    prompt = build_prompt(insight_type, context_reviews)
    return ask_ollama(prompt)
```

---

## ⚡ Phase 6: FastAPI Backend

**File:** `backend/main.py`

```python
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

app = FastAPI(title="Review Intelligence V2 API", version="2.0.0")

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
        platform = detect_platform(request.url)

        if platform == "walmart":
            reviews = scrape_walmart(request.url, request.max_reviews)
        else:
            return {"status": "error", "message": f"Platform '{platform}' not supported yet."}

        if not reviews:
            return {"status": "error", "message": "No reviews found for this product."}

        store_reviews(reviews)

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
```

---

## 🖥️ Phase 7: Streamlit Frontend

**File:** `app.py`

The Streamlit app provides:
- URL input box for any supported marketplace
- "Fetch & Analyze Reviews" button
- Metrics: reviews loaded, average rating, % 4-5 star
- 5 insight tabs: Summary, Complaints, Praises, Recommendations, Root Cause
- Custom Q&A — ask anything about the reviews
- "Reviews used as context" expander showing RAG sources

**Key pattern — Streamlit calls FastAPI:**
```python
# Streamlit sends URL to FastAPI
response = httpx.post(
    "http://localhost:8000/api/reviews/scrape",
    json={"url": url, "max_reviews": max_reviews},
    timeout=180.0
)

# FastAPI scrapes → embeds → stores → returns stats
data = response.json()
st.success(f"✅ Fetched {data['review_count']} reviews!")
```

---

## 🚀 Running the App

You need **2 terminals** open simultaneously. Ollama starts automatically on Windows.

**Terminal 1 — FastAPI Backend:**
```powershell
.venv\Scripts\activate
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Streamlit UI:**
```powershell
.venv\Scripts\activate
streamlit run app.py
```

**Open browser at:** `http://localhost:8501`

---

## 🧪 Testing Checklist

```
[ ] Walmart URL → reviews fetch → all 5 insight tabs generate
[ ] Custom question → relevant AI answer returned
[ ] Invalid URL → helpful error message shown
[ ] ChromaDB persists between restarts
[ ] FastAPI /docs page shows all endpoints
[ ] Health check returns {"status": "ok"}

Coming soon:
[ ] Etsy URL → reviews fetch → insights generate
[ ] Amazon URL → reviews fetch → insights generate
```

---

## 📊 Architecture

```
User (Browser)
      │
      ▼
Streamlit UI — app.py
localhost:8501
      │  HTTP POST requests via httpx
      ▼
FastAPI Backend — backend/main.py
localhost:8000
      │
      ├──► scrapers/detector.py (detect platform)
      │         │
      │    ┌────┴────────────────┐
      │    ▼                     ▼
      │  scrapers/           scrapers/
      │  walmart.py          etsy.py / amazon.py
      │  (RapidAPI)         (Official API / RapidAPI)
      │         │
      │         ▼
      │  services/embeddings.py
      │  (SentenceTransformers all-MiniLM-L6-v2)
      │  Text → 384-dim vectors
      │         │
      │         ▼
      │  services/vector_store.py
      │  (ChromaDB — persistent on disk)
      │  store_reviews() / search_reviews()
      │         │
      ▼         ▼
  services/llm.py
  build_prompt() → RAG context
      │
      ▼
  Ollama (Mistral 7B)
  localhost:11434
      │
      ▼
  AI Insight → FastAPI → Streamlit Dashboard
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API is running |
| GET | `/docs` | Swagger UI — test all endpoints |
| POST | `/api/reviews/scrape` | Fetch reviews from product URL |
| POST | `/api/insights/generate` | Generate AI insight |
| GET | `/api/reviews/status` | Check if reviews are loaded |

**POST /api/reviews/scrape — Request:**
```json
{
  "url": "https://www.walmart.com/ip/product/123456",
  "max_reviews": 100
}
```

**POST /api/reviews/scrape — Response:**
```json
{
  "status": "success",
  "platform": "walmart",
  "review_count": 100,
  "avg_rating": 4.27,
  "high_rated_pct": 85
}
```

**POST /api/insights/generate — Request:**
```json
{
  "insight_type": "complaints"
}
```

Valid insight types: `summary` `complaints` `praises` `recommendations` `root_cause`

---

## 🔑 API Keys Used

| Service | Purpose | Cost | Where to Get |
|---------|---------|------|-------------|
| RapidAPI — Real-Time Walmart Data | Walmart reviews | Free (BASIC) | rapidapi.com |
| Etsy Open API | Etsy reviews | Free (5K/day) | etsy.com/developers |
| Amazon RapidAPI | Amazon reviews | Free tier | rapidapi.com |
| Ollama | Local LLM | Free forever | ollama.com |

---

## 🗺️ Development Roadmap

| Week | Task | Status |
|------|------|--------|
| Week 1 | Walmart scraper + FastAPI + Streamlit | ✅ Complete |
| Week 2 | Etsy scraper (Official API) | ⏳ API pending approval |
| Week 3 | Amazon scraper via RapidAPI | 🔜 Next |
| Week 4 | eBay scraper + competitor comparison | 🔜 Future |
| Week 5 | PDF export + cloud deployment | 🔜 Future |

---

## ✅ Deliverables Checklist

```
✅ pyproject.toml with all dependencies
✅ backend/main.py (FastAPI — all routes)
✅ scrapers/detector.py (platform detection)
✅ scrapers/walmart.py (Walmart via RapidAPI)
⏳ scrapers/etsy.py (Etsy via Official API)
🔜 scrapers/amazon.py (Amazon via RapidAPI)
✅ services/embeddings.py (SentenceTransformers)
✅ services/vector_store.py (ChromaDB)
✅ services/llm.py (Ollama + 5 RAG prompts)
✅ app.py (Streamlit dashboard)
✅ .env (documented — never committed)
✅ .gitignore
✅ RUN_GUIDE_V2.md
⬜ README.md (needs V2 update)
⬜ Architecture diagram (updated for V2)
⬜ GitHub push
```

---

*Built by Hemalatha Mohan | Per Scholas CAP 942 | UCI_3097 AI Solutions Developer*
