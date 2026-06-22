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

## 📌 What It Does

Paste any product URL from a supported marketplace and instantly get AI-powered insights about customer reviews — in seconds, not days.

```
User pastes URL → Live reviews fetched → AI analyzes → Insights displayed
```

### Insight Types

| Tab | What You Get |
|-----|-------------|
| 📋 Summary | 3-paragraph sentiment overview |
| 😤 Complaints | Top 5 most common customer issues |
| 👍 Praises | Top 5 things customers love |
| 💡 Recommendations | 5 actionable product improvements |
| 🔍 Root Cause | Why problems really happen |
| ❓ Custom Q&A | Ask anything about the reviews |

---

## 🏪 Supported Platforms

| Platform | Status | Method |
|----------|--------|--------|
| 🛒 Walmart | ✅ Live | RapidAPI (Real-Time Walmart Data) |
| 🧶 Etsy | ⏳ Pending | Etsy Official Open API v3 |
| 📦 Amazon | 🔜 Next | RapidAPI |
| 🛍️ eBay | 🔜 Future | RapidAPI |

---

## 🏗️ Architecture

```
User (Browser — http://localhost:8501)
              │
              ▼
    ┌─────────────────────┐
    │    Streamlit UI      │  app.py
    │  URL input + tabs    │
    └──────────┬──────────┘
               │ HTTP POST
               ▼
    ┌─────────────────────┐
    │   FastAPI Backend    │  backend/main.py
    │  localhost:8000      │
    └──────────┬──────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
  detector.py      Platform Scrapers
  (detect URL)     walmart.py / etsy.py / amazon.py
                        │
                        ▼ (via RapidAPI / Official APIs)
                   Live Reviews JSON
                        │
                        ▼
              embeddings.py
          (SentenceTransformers)
          Text → 384-dim vectors
                        │
                        ▼
              vector_store.py
              (ChromaDB on disk)
                        │
                        ▼
                   llm.py
              RAG prompt builder
                        │
                        ▼
            Ollama — Mistral 7B
              localhost:11434
                        │
                        ▼
           AI Insights → Dashboard
```

---

## 🛠️ Tools & Technologies

| Category | Tool | Purpose |
|----------|------|---------|
| Language | Python 3.11 | Core language |
| UI | Streamlit | Web dashboard |
| Backend | FastAPI + Uvicorn | REST API |
| LLM | Ollama (Mistral 7B) | Local AI inference |
| Embeddings | SentenceTransformers (MiniLM) | Text → vectors |
| Vector DB | ChromaDB | Semantic search |
| HTTP | httpx | API calls |
| Package Manager | UV | Dependency management |
| Review APIs | RapidAPI + Etsy Open API | Live review data |

> **100% free and open source. No paid APIs. Runs entirely on your local machine.**

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.11 ([download](https://www.python.org/downloads/release/python-3119/))
- [UV](https://astral.sh/uv) package manager
- [Ollama](https://ollama.com) installed
- [RapidAPI](https://rapidapi.com) free account
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

### 5. Install and Set Up Ollama

1. Download from **https://ollama.com**
2. Install it
3. Pull the Mistral model:

```powershell
ollama pull mistral
```

---

### 6. Get Your RapidAPI Key

1. Sign up free at **https://rapidapi.com**
2. Search for **"Real-Time Walmart Data"** by OpenWeb Ninja
3. Subscribe to the **BASIC (free)** plan
4. Copy your API key

---

### 7. Create Your `.env` File

Create a file called `.env` in the project root:

```
RAPIDAPI_KEY=your_rapidapi_key_here
RAPIDAPI_HOST=real-time-walmart-data1.p.rapidapi.com
ETSY_API_KEY=your_etsy_api_key_here
LLM_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
CHROMA_DIR=./data/chroma_db
```

> ⚠️ Never commit your `.env` file to GitHub. It's already in `.gitignore`.

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
2. Paste a supported product URL in the input box
3. Adjust the review count using the sidebar slider
4. Click **"🚀 Fetch & Analyze Reviews"**
5. Wait ~30-60 seconds for reviews to be fetched and embedded
6. Click any insight tab and hit **"Generate"**
7. Use **Step 3: Ask Your Own Question** for custom queries

### Example URLs to Test

**Walmart:**
```
https://www.walmart.com/ip/Neutrogena-Hydro-Boost-Water-Gel-Face-Moisturizer-Lotion-with-Hyaluronic-Acid-1-7-oz/40488263
```

**Etsy (coming soon):**
```
https://www.etsy.com/listing/1797455914/gold-plated-enamel-sakura-flower
```

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
│   ├── walmart.py            ← Walmart scraper (RapidAPI) ✅
│   ├── etsy.py               ← Etsy scraper (Official API) ⏳
│   └── amazon.py             ← Amazon scraper (RapidAPI) 🔜
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

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `http://localhost:8000/health` | Check API is running |
| GET | `http://localhost:8000/docs` | Swagger UI — test endpoints |
| POST | `http://localhost:8000/api/reviews/scrape` | Fetch live reviews from URL |
| POST | `http://localhost:8000/api/insights/generate` | Generate AI insight |
| GET | `http://localhost:8000/api/reviews/status` | Check if reviews are loaded |

---

## ⚠️ Known Limitations

- Ollama must be installed locally (auto-starts on Windows)
- First load takes 60-90 seconds to embed all reviews
- Walmart products need at least some written reviews (not just star ratings)
- Free RapidAPI tier has monthly request limits
- Etsy scraper pending API approval
- Amazon scraper not yet built

---

## 🗺️ Version History

### Version 1 (Capstone Submission)
- CSV dataset → ChromaDB → Ollama → Streamlit
- All 5 insight tabs working
- Custom Q&A

### Version 2 (Current)
- Live review scraping via RapidAPI + Official APIs
- FastAPI backend separating UI from logic
- Walmart scraper working end-to-end
- Etsy and Amazon scrapers in development

---

## 🔜 Planned Features (Version 3)

- [ ] Etsy scraper (Official API — pending approval)
- [ ] Amazon scraper via RapidAPI
- [ ] eBay scraper
- [ ] Competitor comparison across platforms
- [ ] Export insights to PDF report
- [ ] Sentiment trend over time
- [ ] Cloud deployment (Render / Railway)

---

## 🙏 Acknowledgements

- [Ollama](https://ollama.com) — local LLM runtime
- [ChromaDB](https://www.trychroma.com) — vector database
- [SentenceTransformers](https://www.sbert.net) — embedding model
- [Streamlit](https://streamlit.io) — UI framework
- [FastAPI](https://fastapi.tiangolo.com) — backend framework
- [RapidAPI](https://rapidapi.com) — marketplace review APIs
- [Etsy Open API v3](https://developers.etsy.com) — official Etsy data

---

## 📄 License

This project was built as a capstone project for Per Scholas CAP 942 — AI Application Development.

> *"The term 'Etsy' is a trademark of Etsy, Inc. This application uses the Etsy API but is not endorsed or certified by Etsy, Inc."*
