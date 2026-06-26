import httpx
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "real-time-product-search.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY,
}


def extract_product_name(url: str) -> str:
    """Extract product name from Walmart URL."""
    path = urllib.parse.urlparse(url).path
    parts = path.strip("/").split("/")
    if len(parts) >= 2:
        return parts[1].replace("-", " ")
    return "product"


def fetch_reviews(product_id: str, limit: int = 100) -> list[dict]:
    """Fetch reviews with pagination."""
    all_reviews = []
    page = 1
    reviews_per_page = 10

    while len(all_reviews) < limit:
        params = {
            "product_id": product_id,
            "limit": str(reviews_per_page),
            "sort_by": "MOST_RELEVANT",
            "country": "us",
            "language": "en",
            "page": str(page)
        }

        response = httpx.get(
            "https://real-time-product-search.p.rapidapi.com/product-reviews",
            headers=HEADERS,
            params=params,
            timeout=60.0
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        page_reviews = data.get("data", {}).get("reviews", [])

        if not page_reviews:
            print(f"No more reviews at page {page}")
            break

        all_reviews.extend(page_reviews)
        print(f"Page {page}: got {len(page_reviews)} reviews (total: {len(all_reviews)})")

        if len(page_reviews) < reviews_per_page:
            break

        page += 1

    return all_reviews[:limit]


def scrape_walmart(url: str, max_reviews: int = 100) -> tuple:
    """
    Fetch Walmart reviews and product info.
    Returns (reviews, product_info)
    """
    try:
        product_name = extract_product_name(url)
        print(f"Searching for: {product_name}")

        # Search for product
        params = {
            "q": f"{product_name} walmart",
            "country": "us",
            "language": "en",
            "limit": "5"
        }

        response = httpx.get(
            "https://real-time-product-search.p.rapidapi.com/search",
            headers=HEADERS,
            params=params,
            timeout=30.0
        )

        data = response.json()
        products = data.get("data", {}).get("products", [])

        product_info = {}
        product_id = ""

        if products:
            best = products[0]
            photos = best.get("product_photos", [])
            product_id = best.get("product_id", "")
            product_info = {
                "product_name": best.get("product_title", ""),
                "product_image": photos[0] if photos else "",
                "product_price": best.get("price", ""),
                "product_rating": best.get("product_rating", ""),
                "store_name": "Walmart",
            }
            print(f"Found: {product_info['product_name'][:60]}")

        # Fetch reviews
        raw_reviews = fetch_reviews(product_id, limit=max_reviews)

        reviews = []
        for r in raw_reviews:
            body   = r.get("review_text", "") or ""
            title  = r.get("review_title", "") or ""
            rating = r.get("rating", 3) or 3

            if body and len(body) > 10:
                reviews.append({
                    "platform": "walmart",
                    "rating": float(rating),
                    "title": str(title),
                    "body": str(body),
                    "full_text": f"{title}. {body}".strip(),
                })

        print(f"Total reviews: {len(reviews)}")
        return reviews, product_info

    except Exception as e:
        print(f"Error: {e}")
        return [], {}