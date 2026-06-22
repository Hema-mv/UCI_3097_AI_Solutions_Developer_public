import streamlit as st
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="Review Intelligence V2",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Review Intelligence System V2")
st.caption("Paste any Walmart product URL and get AI-powered insights instantly.")

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    max_reviews = st.slider(
        "Max reviews to fetch",
        min_value=20,
        max_value=200,
        value=100,
        step=20
    )
    st.divider()
    st.markdown("**Supported Platforms**")
    st.markdown("✅ Walmart\n🔜 Etsy\n🔜 Amazon")
    st.divider()
    st.markdown("**How it works**")
    st.markdown("""
    1. Paste a product URL
    2. Reviews are fetched live
    3. AI analyzes the reviews
    4. Get instant insights
    """)

# ── Step 1: URL Input ─────────────────────────────────────
st.header("📋 Step 1: Paste a Product URL")

url = st.text_input(
    "Product URL",
    placeholder="https://www.walmart.com/ip/product-name/123456789"
)

if st.button("🚀 Fetch & Analyze Reviews", type="primary") and url:
    with st.spinner("Fetching reviews from Walmart... this may take 30-60 seconds."):
        try:
            response = httpx.post(
                f"{API_BASE}/api/reviews/scrape",
                json={"url": url, "max_reviews": max_reviews},
                timeout=180.0
            )
            data = response.json()

            if data["status"] == "success":
                st.session_state["reviews_loaded"] = True
                st.session_state["platform"] = data["platform"]
                st.session_state["review_count"] = data["review_count"]
                st.session_state["avg_rating"] = data["avg_rating"]

                st.success(f"✅ Fetched {data['review_count']} reviews from {data['platform'].title()}!")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Reviews Fetched", data["review_count"])
                with col2:
                    st.metric("Average Rating", f"{data['avg_rating']} ⭐")
                with col3:
                    st.metric("4-5 Star Reviews", f"{data['high_rated_pct']}%")

            else:
                st.error(f"❌ {data['message']}")

        except httpx.ConnectError:
            st.error("❌ Cannot connect to FastAPI. Make sure uvicorn is running.")

# Status indicator
try:
    status = httpx.get(f"{API_BASE}/api/reviews/status", timeout=5.0).json()
    reviews_ready = status.get("reviews_loaded", False)
except:
    reviews_ready = False

if st.session_state.get("reviews_loaded") or reviews_ready:
    st.info("📊 Reviews ready! Scroll down to generate insights.")
else:
    st.warning("⬆️ Paste a product URL above to get started.")

# ── Step 2: Insights ──────────────────────────────────────
st.header("💡 Step 2: Generate Insights")

if not (st.session_state.get("reviews_loaded") or reviews_ready):
    st.info("Fetch reviews first to unlock insights.")
else:
    tab_labels = [
        "📋 Summary",
        "😤 Complaints",
        "👍 Praises",
        "💡 Recommendations",
        "🔍 Root Cause"
    ]
    insight_keys = [
        "summary",
        "complaints",
        "praises",
        "recommendations",
        "root_cause"
    ]

    tabs = st.tabs(tab_labels)

    for tab, insight_key in zip(tabs, insight_keys):
        with tab:
            if st.button("Generate", key=f"btn_{insight_key}"):
                with st.spinner("Thinking... 30-60 seconds."):
                    try:
                        res = httpx.post(
                            f"{API_BASE}/api/insights/generate",
                            json={"insight_type": insight_key},
                            timeout=120.0
                        )
                        insight = res.json()
                        st.markdown(insight["content"])

                        with st.expander("📄 Reviews used as context"):
                            for i, review in enumerate(insight["supporting_reviews"], 1):
                                st.markdown(f"**Review {i}:** {review[:250]}...")
                                st.divider()

                    except httpx.ConnectError:
                        st.error("❌ Cannot connect to FastAPI.")

# ── Step 3: Custom Question ───────────────────────────────
st.header("❓ Step 3: Ask Your Own Question")

if st.session_state.get("reviews_loaded") or reviews_ready:
    user_question = st.text_input(
        "Ask anything about the reviews",
        placeholder="e.g. What do customers say about the packaging?"
    )

    if st.button("Ask") and user_question:
        with st.spinner("Thinking..."):
            try:
                from services.vector_store import search_reviews
                from services.llm import ask_ollama

                relevant = search_reviews(user_question, n_results=10)
                context = "\n\n".join([f"- {r[:300]}" for r in relevant])
                prompt = f"""Based on these customer reviews, answer this question:
"{user_question}"

REVIEWS:
{context}

ANSWER:"""
                answer = ask_ollama(prompt)
                st.markdown(answer)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")