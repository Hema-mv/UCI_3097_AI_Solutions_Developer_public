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
        print(f"Page {page}: got {len(page_reviews)} (total: {len(all_reviews)})")

        if len(page_reviews) < reviews_per_page:
            break

        page += 1

    return all_reviews[:limit]


def scrape_amazon(url: str, max_reviews: int = 100) -> tuple:
    """
    Fetch Amazon reviews and product info.
    Returns (reviews, product_info)
    """
    from scrapers.detector import extract_amazon_asin

    try:
        # Extract ASIN
        asin = extract_amazon_asin(url)
        print(f"Amazon ASIN: {asin}")

        # Extract product name from URL
        path = urllib.parse.urlparse(url).path
        parts = path.strip("/").split("/")
        product_name = ""
        for part in parts:
            if part != "dp" and len(part) > 5 and not part.startswith("B0"):
                product_name = part.replace("-", " ")
                break

        print(f"Product name: {product_name}")

        # Search for product
        query = f"{product_name} {asin}".strip() if product_name else f"amazon {asin}"
        params = {
            "q": query,
            "country": "us",
            "language": "en",
            "limit": "10"
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
            # Try to find exact ASIN match
            for p in products:
                page_url = p.get("product_page_url", "")
                if asin in page_url or asin in p.get("product_id", ""):
                    best = p
                    break
            else:
                best = products[0]

            photos = best.get("product_photos", [])
            product_id = best.get("product_id", "")
            product_info = {
                "product_name": best.get("product_title", ""),
                "product_image": photos[0] if photos else "",
                "product_price": best.get("price", ""),
                "product_rating": best.get("product_rating", ""),
                "store_name": "Amazon",
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
                    "platform": "amazon",
                    "rating": float(rating),
                    "title": str(title),
                    "body": str(body),
                    "full_text": f"{title}. {body}".strip(),
                })

        print(f"Total Amazon reviews: {len(reviews)}")
        return reviews, product_info

    except Exception as e:
        print(f"❌ Error: {e}")
        return [], {}