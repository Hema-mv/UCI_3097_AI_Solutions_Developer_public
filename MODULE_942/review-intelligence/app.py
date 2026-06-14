import streamlit as st
import pandas as pd
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://localhost:8000"

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Review Intelligence",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Review Intelligence System")
st.caption("Analyze customer reviews and get AI-powered insights instantly.")

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    max_rows = st.slider(
        "Number of reviews to load",
        min_value=100,
        max_value=1000,
        value=300,
        step=100
    )
    st.divider()
    st.markdown("**How it works**")
    st.markdown("""
    1. Load your reviews CSV
    2. Reviews are embedded and stored
    3. Choose an insight type
    4. AI analyzes relevant reviews
    """)

# ── Step 1: Load Reviews ──────────────────────────────────
st.header("📂 Step 1: Load Your Reviews")

use_default = st.checkbox("Use default dataset (data/reviews.csv)", value=True)

if st.button("Load & Process Reviews", type="primary"):
    with st.spinner("Loading and processing reviews... this may take a minute."):
        try:
            response = httpx.post(
                f"{API_BASE}/api/reviews/load",
                json={
                    "csv_path": "data/reviews.csv",
                    "max_rows": max_rows
                },
                timeout=120.0
            )
            data = response.json()

            if data["status"] == "success":
                st.session_state["reviews_loaded"] = True
                st.session_state["review_count"] = data["review_count"]
                st.session_state["avg_rating"] = data["avg_rating"]

                st.success(f"✅ Loaded and stored {data['review_count']} reviews!")

                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Reviews Loaded", data["review_count"])
                with col2:
                    st.metric("Average Rating", f"{data['avg_rating']} ⭐")
                with col3:
                    st.metric("Status", "Ready ✅")
            else:
                st.error("Something went wrong loading reviews.")

        except httpx.ConnectError:
            st.error("❌ Cannot connect to FastAPI. Make sure uvicorn is running.")

# Status indicator
status_response = None
try:
    status_response = httpx.get(f"{API_BASE}/api/reviews/status", timeout=5.0)
    reviews_ready = status_response.json()["reviews_loaded"]
except:
    reviews_ready = False

if st.session_state.get("reviews_loaded") or reviews_ready:
    st.info("📊 Reviews are ready for analysis. Scroll down to generate insights.")
else:
    st.warning("⬆️ Load reviews above before generating insights.")

# ── Step 2: Insights ──────────────────────────────────────
st.header("💡 Step 2: Generate Insights")

if not (st.session_state.get("reviews_loaded") or reviews_ready):
    st.info("Load reviews first to unlock insights.")
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
                with st.spinner("Searching reviews and thinking... 30-60 seconds."):
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
                        st.error("❌ Cannot connect to FastAPI. Make sure uvicorn is running.")

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
                res = httpx.post(
                    f"{API_BASE}/api/insights/generate",
                    json={"insight_type": user_question},
                    timeout=120.0
                )
                st.markdown(res.json().get("content", "No response"))
            except httpx.ConnectError:
                st.error("❌ Cannot connect to FastAPI. Make sure uvicorn is running.")