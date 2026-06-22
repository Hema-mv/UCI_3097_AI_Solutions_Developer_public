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
    User just pastes a Walmart URL — everything else is automatic.
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
                print(f"API error: {response.status_code} — {response.text[:200]}")
                break

            data = response.json()

            # Extract reviews from response
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

            # Be polite — small delay between requests
            time.sleep(0.5)

        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    print(f"Total reviews fetched: {len(reviews)}")
    return reviews[:max_reviews]