# 🔍 AI Multi Marketplace Review Intelligence System
### Version 2 — Live Scraping Edition

> **Capstone Project — Per Scholas Software Engineering / AI Track (CAP 942)**  
> **Student:** Hemalatha Mohan  
> **Program:** UCI_3097 AI Solutions Developer | MODULE 942

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0-green)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-Mistral_7B-orange)](https://ollama.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-purple)](https://trychroma.com)

---

## 🧠 What Is This Project?

The **AI Multi Marketplace Review Intelligence System** is an AI-powered application that automatically collects customer reviews from e-commerce marketplaces and turns them into actionable business insights using a local large language model (LLM).

Instead of a seller manually reading hundreds of reviews across multiple platforms, this system does it in seconds — fetching live reviews, analyzing them with AI, and presenting clear, structured insights in a web dashboard — **complete with product images, pricing, and store information.**

---

## 🎯 Who Is This For?

| User | How They Use It |
|------|----------------|
| **E-commerce sellers** | Understand what customers love and hate about their products without reading 500 reviews manually |
| **Brand managers** | Monitor product reputation across Walmart, Etsy, and Amazon in one place |
| **Product managers** | Get AI-generated improvement recommendations based on real customer feedback |
| **Market researchers** | Quickly analyze competitor products and identify market gaps |
| **Entrepreneurs** | Validate product ideas by analyzing what customers wish existed |

---

## 💡 Why Does This Exist?

**Before this app:**
```
❌ Read 500+ reviews one by one — takes days
❌ Reviews spread across multiple platforms — no unified view
❌ Hard to spot patterns — easy to miss recurring issues
❌ Amazon/Walmart built-in summaries are shallow — designed for shoppers, not sellers
❌ No tool tells you WHY problems happen or WHAT to improve
```

**After this app:**
```
✅ Paste a product URL
✅ See the product image, name, price instantly
✅ Get AI analysis in 60 seconds
✅ Know the top 5 complaints with real examples
✅ Know the top 5 praises customers love
✅ Get 5 specific product improvement suggestions
✅ Understand root causes — not just surface complaints
✅ Ask any question and get an answer based on real reviews
```

**Real example:** A Walmart seller sees that 30% of negative reviews mention "packaging issues." Without this app, they'd need to read hundreds of reviews to spot this pattern. With this app, it takes one click — and the AI also explains that the root cause is "insufficient bubble wrap for glass containers during shipping." That insight directly leads to a business decision that reduces returns and increases sales.

---

## 🆚 How Is This Different From Walmart/Amazon's Built-In Reviews?

| Feature | Walmart/Amazon Website | This App |
|---------|----------------------|----------|
| See individual reviews | ✅ | ✅ |
| Product image + price shown | ✅ | ✅ |
| Analyze 100+ reviews at once | ❌ | ✅ |
| Top 5 complaints summary | ❌ | ✅ |
| Top 5 praises summary | ❌ | ✅ |
| Root cause analysis | ❌ | ✅ |
| Product improvement suggestions | ❌ | ✅ |
| Ask custom questions | ❌ | ✅ |
| Works across multiple platforms | ❌ | ✅ |
| Runs locally — no data sent to cloud | ❌ | ✅ |

---

## 🤖 How the AI Works — RAG Explained

This app uses **RAG (Retrieval Augmented Generation)** — one of the most important techniques in modern AI applications.

### The Problem with Regular AI

If you just ask an AI "what do customers complain about this product?" — it **guesses** based on its training data. The answer might be wrong, outdated, or completely made up (called "hallucination").

### How RAG Fixes This

RAG gives the AI **real data to read** before answering:

```
STEP 1 — RETRIEVE
User clicks "Generate Complaints"
        ↓
ChromaDB searches for the 15 most relevant reviews
about "problems issues broken disappointed"
using semantic search (meaning-based, not keyword-based)
        ↓
Returns 15 real customer reviews

STEP 2 — AUGMENT
Those 15 real reviews are injected into the prompt:

"Here are 15 real customer reviews:
 - Box arrived completely crushed
 - Smell is way too strong for sensitive skin
 - Works great but way overpriced
 Now list the top 5 complaints..."

STEP 3 — GENERATE
Mistral 7B reads the ACTUAL reviews
and generates insights based on what
customers REALLY said — not guesses
```

### Side By Side Example

| | Without RAG | With RAG (This App) |
|--|-------------|-------------------|
| Source | AI training data (old) | Real customer reviews (current) |
| Answer | "Customers typically report skin reactions..." | "1. Packaging — boxes arrive crushed during shipping" |
| Accuracy | Guesses | Based on real facts |
| Specific to product | ❌ Generic | ✅ Product-specific |
| Hallucination risk | High | Very low |

### Why This Matters

> The AI in this app never guesses. Every insight it generates is backed by actual customer reviews retrieved from ChromaDB. This is what makes the insights specific, accurate, and trustworthy.

---

## 🔍 How Semantic Search Works

When a user clicks "Generate Complaints" the app doesn't just search for the word "complaint." It uses **semantic search** — searching by meaning.

```
Search query: "problem issue broken disappointed negative"
        ↓
SentenceTransformers converts to 384 numbers:
[0.12, -0.34, 0.91, 0.05, ...]
        ↓
ChromaDB finds reviews whose numbers are closest
        ↓
Finds reviews like:
✅ "Box arrived completely crushed"       ← didn't use the word "problem"
✅ "Stopped working after 2 days"         ← didn't use the word "issue"
✅ "Completely let down by this product"  ← didn't use the word "disappointed"
```

Keyword search would miss all three of those. Semantic search finds them all.

---

## ⚡ What FastAPI Does

FastAPI is the **middle layer** between your Streamlit UI and your AI pipeline — like a waiter between a customer and the kitchen.

```
Streamlit UI (customer)
      ↓ sends request
FastAPI Backend (waiter)
      ↓ coordinates everything
Scrapers + ChromaDB + Ollama (kitchen)
      ↓ sends result back
FastAPI Backend (waiter)
      ↓ returns response
Streamlit UI (customer sees result)
```

**Your 3 FastAPI endpoints:**

| Endpoint | What It Does |
|----------|-------------|
| `POST /api/reviews/scrape` | Detects platform → scrapes reviews → stores in ChromaDB → returns product info + image |
| `POST /api/insights/generate` | Searches ChromaDB → builds RAG prompt → calls Ollama → returns AI insight |
| `GET /api/reviews/status` | Checks if reviews are loaded in ChromaDB |

Test all endpoints visually at: `http://localhost:8000/docs`

---

## 📌 What It Does

Paste any product URL from a supported marketplace and instantly get:
- 🖼️ Product image, name, price and store
- 🤖 AI-powered insights from real customer reviews

```
User pastes URL
      ↓
Product image + info fetched
      ↓
Live reviews fetched from marketplace
      ↓
Reviews embedded → stored in ChromaDB
      ↓
User clicks insight tab
      ↓
ChromaDB retrieves relevant reviews (RAG)
      ↓
Mistral reads reviews → generates insight
      ↓
Result displayed in dashboard
```

### Insight Types

| Tab | What You Get |
|-----|-------------|
| 📋 Summary | 3-paragraph sentiment overview of all reviews |
| 😤 Complaints | Top 5 most common customer issues with examples |
| 👍 Praises | Top 5 things customers love about the product |
| 💡 Recommendations | 5 specific product improvement suggestions |
| 🔍 Root Cause | Deep analysis of WHY problems happen |
| ❓ Custom Q&A | Ask anything — "Does it have SPF?" "Is packaging good?" |

---

## 🏪 Supported Platforms

| Platform | Status | Method |
|----------|--------|--------|
| 🛒 Walmart | ✅ Live | Real-Time Product Search API |
| 📦 Amazon | ✅ Live | Real-Time Product Search API |
| 🧶 Etsy | ✅ Live | Real-Time Product Search API |
| 🛍️ eBay | 🔜 Future | To be added |

---

## 🧪 Try These URLs Right Now

Copy and paste any of these into the app to test immediately:

### 🛒 Walmart
```
https://www.walmart.com/ip/Neutrogena-Hydro-Boost-Water-Gel-Face-Moisturizer-Lotion-with-Hyaluronic-Acid-1-7-oz/40488263
```
```
https://www.walmart.com/ip/Comfier-Full-Body-Back-Massager-with-Heating-10-Soothing-Vibration-Back-Massage-Pad-for-Pain-Relief-Massage-Mat-Gifts/5344517922
```
```
https://www.walmart.com/ip/IronMax-13Amp-Corded-Scarifier-15-Electric-Lawn-Dethatcher-w-50L-Collection-Bag-Orange/765224053
```

### 📦 Amazon
```
https://www.amazon.com/Amazon-Echo-Spot-2024-release/dp/B0BFC7WQ6R
```
```
https://www.amazon.com/Neutrogena-Hydrating-Facial-Moisturizer/dp/B00NR1YQG6
```

### 🧶 Etsy
```
https://www.etsy.com/listing/1665810180/linen-shower-curtain-livingroom-curtain
```
```
https://www.etsy.com/listing/1797455914/gold-plated-enamel-sakura-flower
```

---

## 🏗️ Architecture

```
User (Browser — http://localhost:8501)
              │
              ▼
    ┌─────────────────────┐
    │    Streamlit UI      │  app.py
    │  URL input + tabs    │
    │  Product image shown │
    └──────────┬──────────┘
               │ HTTP POST
               ▼
    ┌─────────────────────┐
    │   FastAPI Backend    │  backend/main.py
    │   localhost:8000     │
    └──────────┬──────────┘
               │
       ┌───────┴──────────────┐
       ▼                      ▼
  detector.py           Platform Scrapers
  (detect platform)     walmart.py
                        amazon.py
                        etsy.py
                             │
                             ▼
               Real-Time Product Search API
               (reviews + product image + price)
                             │
                             ▼
                   embeddings.py
               (SentenceTransformers)
               Text → 384-dim vectors
                             │
                             ▼
                   vector_store.py
                   (ChromaDB on disk)
                    Semantic Search
                             │
                             ▼
                        llm.py
                   RAG prompt builder
                   (injects real reviews)
                             │
                             ▼
               Ollama — Mistral 7B
                 localhost:11434
                 (local AI — no internet)
                             │
                             ▼
          AI Insights + Product Image → Dashboard
```

---

## 🛠️ Tools & Technologies

| Category | Tool | Purpose |
|----------|------|---------|
| Language | Python 3.11 | Core language |
| UI | Streamlit | Web dashboard with product images |
| Backend | FastAPI + Uvicorn | REST API — middle layer between UI and AI |
| LLM | Ollama (Mistral 7B) | Local AI inference — no cloud, no cost, no data sharing |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) | Converts text to 384-dim meaning vectors |
| Vector DB | ChromaDB | Stores embeddings + enables semantic search |
| RAG | ChromaDB + Ollama | Retrieves real reviews → feeds to AI for accurate insights |
| HTTP client | httpx | API calls to RapidAPI |
| Package Manager | UV | Fast Python dependency management |
| Review API | Real-Time Product Search (RapidAPI) | Live reviews + product images for Walmart, Amazon, Etsy |

> **100% free and open source. Runs entirely on your local machine. No data sent to cloud.**

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.11 ([download](https://www.python.org/downloads/release/python-3119/))
- [UV](https://astral.sh/uv) package manager
- [Ollama](https://ollama.com) installed
- [RapidAPI](https://rapidapi.com) free account (100 requests/month free)
- 16GB RAM recommended

---

### 1. Clone the Repository

```bash
git clone https://github.com/Hema-mv/UCI_3097_AI_Solutions_Developer_public.git
cd UCI_3097_AI_Solutions_Developer_public/MODULE_942/review-intelligence-v2
```

---

### 2. Install UV

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### 3. Create Virtual Environment

```powershell
uv venv --python 3.11
.venv\Scripts\activate        # Windows
# OR
source .venv/bin/activate     # Mac/Linux
```

---

### 4. Install Dependencies

```powershell
uv add fastapi uvicorn streamlit sentence-transformers chromadb pandas python-dotenv httpx spacy playwright
uv run playwright install chromium
uv run python -m spacy download en_core_web_sm
```

---

### 5. Install Ollama and Pull Mistral

1. Download from **https://ollama.com**
2. Install it like a normal Windows app
3. Pull the Mistral model (~4GB):

```powershell
ollama pull mistral
```

---

### 6. Get Your RapidAPI Key

1. Sign up free at **https://rapidapi.com**
2. Search for **"Real-Time Product Search"**
3. Subscribe to the **BASIC ($0.00/month)** plan
4. Copy your API key

---

### 7. Create Your `.env` File

```
RAPIDAPI_KEY=your_rapidapi_key_here
LLM_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
CHROMA_DIR=./data/chroma_db
```

> ⚠️ Never commit your `.env` file to GitHub. It is already in `.gitignore`.

---

## 🚀 Running the App

Open **2 terminals** in VS Code (**Ctrl + `**, then click **+**):

**Terminal 1 — Start FastAPI:**
```powershell
.venv\Scripts\activate
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Start Streamlit:**
```powershell
.venv\Scripts\activate
streamlit run app.py
```

> **Note:** Ollama starts automatically on Windows.

Open browser at: `http://localhost:8501`

---

## 📖 How to Use

1. Open `http://localhost:8501`
2. Paste any supported product URL
3. Adjust review count using the sidebar slider (20–200)
4. Click **"🚀 Fetch & Analyze Reviews"**
5. See the **product image, name, price** displayed automatically
6. Click any insight tab → hit **"Generate"**
7. Use **Step 3** to ask your own questions

---

## 📁 Project Structure

```
review-intelligence-v2/
├── app.py                    ← Streamlit UI
├── pyproject.toml            ← UV dependencies
├── .env                      ← API keys (not committed)
├── .gitignore
├── README.md
│
├── backend/
│   └── main.py               ← FastAPI backend
│
├── scrapers/
│   ├── detector.py           ← Detects platform from URL
│   ├── walmart.py            ← Walmart scraper ✅
│   ├── etsy.py               ← Etsy scraper ✅
│   └── amazon.py             ← Amazon scraper ✅
│
├── services/
│   ├── embeddings.py         ← SentenceTransformers
│   ├── vector_store.py       ← ChromaDB store + search
│   └── llm.py                ← Ollama + RAG prompts
│
└── data/
    └── chroma_db/            ← Vector database (auto-created)
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API is running |
| GET | `/docs` | Swagger UI — test all endpoints |
| POST | `/api/reviews/scrape` | Fetch live reviews + product info |
| POST | `/api/insights/generate` | Generate AI insight using RAG |
| GET | `/api/reviews/status` | Check if reviews are loaded |

---

## ⚠️ Known Limitations

- Ollama must be installed locally (auto-starts on Windows)
- First load takes 60-90 seconds to embed all reviews
- Free RapidAPI tier has 100 requests/month limit
- Products need written reviews (not just star ratings)
- AI insights quality depends on review count and quality

---

## 🗺️ Version History

### Version 1 (Capstone Submission ✅)
- Amazon Fine Food Reviews CSV dataset
- SentenceTransformers + ChromaDB + Ollama
- All 5 insight tabs + Custom Q&A

### Version 2 (Current ✅)
- ✅ Live scraping — Walmart, Amazon, Etsy
- ✅ Product image + name + price display
- ✅ FastAPI backend
- ✅ Single API for all 3 platforms
- ✅ RAG pipeline with semantic search

---

## 🔜 Planned Features (Version 3)

- [ ] eBay scraper
- [ ] Competitor product comparison
- [ ] Export insights to PDF
- [ ] Sentiment trend chart
- [ ] Cloud deployment

---

## 🙏 Acknowledgements

- [Ollama](https://ollama.com) — local LLM runtime
- [ChromaDB](https://www.trychroma.com) — vector database
- [SentenceTransformers](https://www.sbert.net) — embedding model
- [Streamlit](https://streamlit.io) — UI framework
- [FastAPI](https://fastapi.tiangolo.com) — backend framework
- [RapidAPI — Real-Time Product Search](https://rapidapi.com) — live review data

---

## 📄 License

Built as a capstone project for Per Scholas CAP 942 — AI Application Development.

> *This application uses third-party APIs to retrieve publicly available product review data. Walmart, Amazon, and Etsy are trademarks of their respective owners. This application is not affiliated with or endorsed by any of these companies.*
