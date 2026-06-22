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
        return "❌ Could not connect to Ollama. Make sure it is running: ollama serve"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def build_prompt(insight_type: str, context_reviews: list[str]) -> str:
    """Build a prompt using retrieved reviews as context."""
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
- State the issue in one sentence
- Give one short example from the reviews

CUSTOMER REVIEWS:
{context}

TOP COMPLAINTS:""",

        "praises": f"""List the TOP 5 things customers praise most from these reviews.
For each praise:
- State what they love in one sentence
- Give one short example from the reviews

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
    """Full pipeline: build prompt → call Ollama → return result."""
    prompt = build_prompt(insight_type, context_reviews)
    return ask_ollama(prompt)