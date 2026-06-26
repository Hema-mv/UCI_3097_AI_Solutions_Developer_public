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

This project combines several advanced AI and software engineering concepts:

- **RAG (Retrieval Augmented Generation)** — the AI doesn't guess. It reads actual customer reviews before generating insights.
- **Semantic Search** — finds reviews by meaning, not just keywords. Searching "battery problems" also finds reviews that say "died after 2 days."
- **Local LLM** — runs entirely on your own computer using Ollama. No internet connection needed for AI. No API costs. No data privacy concerns.
- **Live Data Scraping** — fetches real, current reviews directly from marketplaces via APIs.
- **Product Image Display** — shows the actual product photo alongside insights.

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

E-commerce sellers face a real problem:

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

Walmart and Amazon show you **raw data**. This app gives you **actionable intelligence.**

---

## 📌 What It Does

Paste any product URL from a supported marketplace and instantly get:
- 🖼️ Product image, name, price and store
- 🤖 AI-powered insights from real customer reviews

```
User pastes URL → Product image fetched → Live reviews fetched → AI analyzes → Insights displayed
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

## 🏗️ How It Works (Architecture)

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
       ┌───────┴────────────────────┐
       ▼                            ▼
  detector.py                Platform Scrapers
  (detect URL platform)      walmart.py
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
| Backend | FastAPI + Uvicorn | REST API |
| LLM | Ollama (Mistral 7B) | Local AI inference — no cloud needed |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) | Text → 384-dim vectors |
| Vector DB | ChromaDB | Semantic search + persistent storage |
| HTTP client | httpx | API calls |
| Package Manager | UV | Fast Python dependency management |
| Review API | Real-Time Product Search (RapidAPI) | Live reviews + product images for Walmart, Amazon, Etsy |

> **100% free and open source. Runs entirely on your local machine.**

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
3. Subscribe to the **BASIC ($0.00/month)** plan — 100 requests/month free
4. Copy your API key

---

### 7. Create Your `.env` File

Create a file called `.env` in the project root:

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

> **Note:** Ollama starts automatically on Windows. No need to run it manually.

Open your browser at:
```
http://localhost:8501
```

---

## 📖 How to Use

1. Open `http://localhost:8501` in your browser
2. Paste any supported product URL in the input box
3. Adjust the review count using the sidebar slider (20–200)
4. Click **"🚀 Fetch & Analyze Reviews"**
5. See the **product image, name, price** displayed automatically
6. Wait ~30-60 seconds for reviews to be fetched and processed
7. Click any insight tab and hit **"Generate"**
8. Use **Step 3: Ask Your Own Question** for custom queries

---

## 📁 Project Structure

```
review-intelligence-v2/
├── app.py                    ← Streamlit UI (main entry point)
├── pyproject.toml            ← UV dependencies
├── .env                      ← API keys (not committed)
├── .gitignore
├── README.md
├── IMPLEMENTATION_GUIDE_V2.md
├── RUN_GUIDE_V2.md
│
├── backend/
│   ├── __init__.py
│   └── main.py               ← FastAPI backend (all routes)
│
├── scrapers/
│   ├── __init__.py
│   ├── detector.py           ← Detects platform from URL
│   ├── walmart.py            ← Walmart scraper ✅
│   ├── etsy.py               ← Etsy scraper ✅
│   └── amazon.py             ← Amazon scraper ✅
│
├── services/
│   ├── __init__.py
│   ├── embeddings.py         ← SentenceTransformers
│   ├── vector_store.py       ← ChromaDB store + search
│   └── llm.py                ← Ollama + RAG prompts
│
└── data/
    └── chroma_db/            ← Auto-created vector database
```

---

## 🌐 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API is running |
| GET | `/docs` | Swagger UI — test all endpoints |
| POST | `/api/reviews/scrape` | Fetch live reviews + product info from URL |
| POST | `/api/insights/generate` | Generate AI insight |
| GET | `/api/reviews/status` | Check if reviews are loaded |

---

## ⚠️ Known Limitations

- Ollama must be installed locally (auto-starts on Windows)
- First load takes 60-90 seconds to embed all reviews
- Free RapidAPI tier has 100 requests/month limit
- Products need written reviews (not just star ratings) for best results
- AI insights are based on fetched reviews — quality depends on review count

---

## 🗺️ Version History

### Version 1 (Capstone Submission ✅)
Built during the Per Scholas CAP 942 capstone:
- Amazon Fine Food Reviews CSV dataset
- SentenceTransformers embeddings
- ChromaDB vector store
- Ollama + Mistral RAG pipeline
- All 5 insight tabs working
- Custom Q&A

### Version 2 (Current ✅)
Post-capstone development:
- ✅ Live review scraping — Walmart, Amazon, Etsy
- ✅ Product image display
- ✅ Product name, price, store info
- ✅ FastAPI backend
- ✅ URL-based input instead of CSV upload
- ✅ Single API for all 3 platforms

---

## 🔜 Planned Features (Version 3)

- [ ] eBay scraper
- [ ] Side-by-side competitor product comparison
- [ ] Export insights to PDF report
- [ ] Sentiment trend chart over time
- [ ] Support multiple products simultaneously
- [ ] Cloud deployment (Render / Railway)

---

## 🙏 Acknowledgements

- [Ollama](https://ollama.com) — local LLM runtime
- [ChromaDB](https://www.trychroma.com) — vector database
- [SentenceTransformers](https://www.sbert.net) — embedding model
- [Streamlit](https://streamlit.io) — UI framework
- [FastAPI](https://fastapi.tiangolo.com) — backend framework
- [RapidAPI — Real-Time Product Search](https://rapidapi.com) — live review data + product images

---

## 📄 License

This project was built as a capstone project for Per Scholas CAP 942 — AI Application Development.

> *This application uses third-party APIs to retrieve publicly available product review data. Walmart, Amazon, and Etsy are trademarks of their respective owners. This application is not affiliated with or endorsed by any of these companies.*
