# 🚀 Review Intelligence V2 — Run Guide

> **Quick reference for running and working on your project every day.**

---

## 📁 Project Location

```
C:\Per-Scholas\2026_CAX_142\UCI_3097_AI_Solutions_Developer_public\MODULE_942\review-intelligence-v2\
```

---

## ▶️ How to Run the App (Every Time)

### Step 1 — Open VS Code
```powershell
cd C:\Per-Scholas\2026_CAX_142\UCI_3097_AI_Solutions_Developer_public\MODULE_942\review-intelligence-v2
code .
```

### Step 2 — Open 2 Terminals in VS Code
Press **Ctrl + `** to open terminal, then click **+** to add a second one.

---

### Terminal 1 — Start FastAPI Backend
```powershell
.venv\Scripts\activate
uvicorn backend.main:app --reload --port 8000
```

✅ You should see:
```
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

---

### Terminal 2 — Start Streamlit UI
```powershell
.venv\Scripts\activate
streamlit run app.py
```

✅ You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

### Step 3 — Open Browser
```
http://localhost:8501
```

> **Note:** Ollama starts automatically on Windows. You do NOT need to run `ollama serve` manually.

---

## 🧪 Test URLs

Use these to test your app:

### Walmart (Working ✅)
```
https://www.walmart.com/ip/Neutrogena-Hydro-Boost-Water-Gel-Face-Moisturizer-Lotion-with-Hyaluronic-Acid-1-7-oz/40488263
```
```
https://www.walmart.com/ip/Oribe-Gold-Lust-Repair-Restore-Conditioner-33-8-oz/155132018
```

### Etsy (In Progress 🔨)
```
https://www.etsy.com/listing/1797455914/gold-plated-enamel-sakura-flower
```

### Amazon (Coming Soon 🔜)
```
https://www.amazon.com/dp/B08N5WRWNW
```

---

## 🛑 How to Stop the App

In each terminal press:
```
Ctrl + C
```

---

## 🔑 API Keys & Config

Your `.env` file (never share this):
```
RAPIDAPI_KEY=122fd227e1msh6787ed91be7b080p1a764djsn7e79ba4d6c3c
RAPIDAPI_HOST=real-time-walmart-data1.p.rapidapi.com
LLM_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
CHROMA_DIR=./data/chroma_db
```

---

## 📁 Project Structure

```
review-intelligence-v2/
├── app.py                  ← Streamlit UI (main entry point)
├── pyproject.toml          ← UV dependencies
├── .env                    ← API keys and config (never commit!)
├── .gitignore
│
├── backend/
│   ├── __init__.py
│   └── main.py             ← FastAPI backend (localhost:8000)
│
├── scrapers/
│   ├── __init__.py
│   ├── detector.py         ← Detects platform from URL
│   ├── walmart.py          ← Walmart scraper (RapidAPI) ✅
│   ├── etsy.py             ← Etsy scraper 🔨
│   └── amazon.py           ← Amazon scraper 🔜
│
├── services/
│   ├── __init__.py
│   ├── embeddings.py       ← SentenceTransformers
│   ├── vector_store.py     ← ChromaDB
│   └── llm.py              ← Ollama + RAG prompts
│
└── data/
    └── chroma_db/          ← Vector database (auto-created)
```

---

## 🔄 Architecture

```
User pastes URL (Walmart / Etsy / Amazon)
              ↓
      Streamlit UI (app.py)
      localhost:8501
              ↓
      FastAPI Backend (backend/main.py)
      localhost:8000
              ↓
      Platform Detector (scrapers/detector.py)
         ↙         ↓         ↘
  Walmart      Etsy        Amazon
  scraper      scraper     scraper
  (RapidAPI)  (RapidAPI)  (RapidAPI)
              ↓
      services/embeddings.py
      (SentenceTransformers — all-MiniLM-L6-v2)
              ↓
      services/vector_store.py
      (ChromaDB — semantic search)
              ↓
      services/llm.py
      (RAG prompt builder)
              ↓
      Ollama (Mistral 7B)
      localhost:11434
              ↓
      AI Insights → Streamlit Dashboard
```

---

## 🌐 API Endpoints

| Method | URL | What it does |
|--------|-----|-------------|
| GET | http://localhost:8000/health | Check if API is running |
| GET | http://localhost:8000/docs | View all endpoints (Swagger UI) |
| POST | http://localhost:8000/api/reviews/scrape | Fetch reviews from URL |
| POST | http://localhost:8000/api/insights/generate | Generate AI insight |
| GET | http://localhost:8000/api/reviews/status | Check if reviews are loaded |

---

## 💡 Insight Types

| Tab | insight_type value |
|-----|-------------------|
| 📋 Summary | `summary` |
| 😤 Complaints | `complaints` |
| 👍 Praises | `praises` |
| 💡 Recommendations | `recommendations` |
| 🔍 Root Cause | `root_cause` |

---

## 🛒 Platform Status

| Platform | Method | Status |
|----------|--------|--------|
| Walmart | RapidAPI (Real-Time Walmart Data) | ✅ Working |
| Etsy | RapidAPI / Etsy Official API | 🔨 In Progress |
| Amazon | RapidAPI | 🔜 Next |
| eBay | RapidAPI | 🔜 Future |

---

## 🐛 Common Errors & Fixes

### ❌ "Cannot connect to FastAPI"
```
Fix: Make sure uvicorn is running in Terminal 1
Run: uvicorn backend.main:app --reload --port 8000
```

### ❌ "Could not connect to Ollama"
```
Fix: Ollama should auto-start on Windows
Check: Open Task Manager and look for Ollama
Or run: ollama serve (in a separate terminal)
```

### ❌ "No reviews found"
```
Fix: Try a different product URL
Make sure the product has written reviews (not just star ratings)
```

### ❌ "ModuleNotFoundError"
```
Fix: Make sure venv is activated
Run: .venv\Scripts\activate
```

### ❌ PowerShell execution policy error
```
Fix: Run this once:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📦 Install Dependencies (First Time Only)

```powershell
uv venv --python 3.11
.venv\Scripts\activate
uv add fastapi uvicorn streamlit sentence-transformers chromadb pandas python-dotenv httpx spacy playwright
uv run playwright install chromium
uv run python -m spacy download en_core_web_sm
```

---

## 🔃 Push to GitHub

```powershell
cd C:\Per-Scholas\2026_CAX_142\UCI_3097_AI_Solutions_Developer_public
git add MODULE_942/review-intelligence-v2/
git commit -m "Add V2 - Live Walmart scraper via RapidAPI"
git push origin main
```

---

## 📅 Development Roadmap

| Week | Task | Status |
|------|------|--------|
| Week 1 | Walmart scraper + FastAPI + Streamlit | ✅ Done |
| Week 2 | Etsy scraper | 🔨 In Progress |
| Week 3 | Amazon scraper via RapidAPI | 🔜 Next |
| Week 4 | eBay scraper + competitor comparison | 🔜 Future |
| Week 5 | PDF export + deploy online | 🔜 Future |

---

## 🧪 Quick Test Commands

```powershell
# Test Walmart scraper only
uv run python test_walmart.py

# Test Etsy scraper only
uv run python test_etsy.py

# Test full pipeline
uv run python test_walmart.py
```

---

*Save this file — refer to it every time you start working on the project.*
