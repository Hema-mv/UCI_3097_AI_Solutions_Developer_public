import httpx
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

headers = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "real-time-product-search.p.rapidapi.com",
    "x-rapidapi-key": RAPIDAPI_KEY,
}

# Complete product ID from RapidAPI example
product_id = "catalogid:8425421641323327810,gpcid:1261873578657646759,headlineOfferDocid:6367138647863486978,rds:PC_1261873578657646759|PROD_PC_1261873578657646759,imageDocid:17958223083723421156,mid:576462516936404275,pvt:hg,pvf:"

params = {
    "product_id": product_id,
    "limit": "10",
    "sort_by": "MOST_RELEVANT",
    "country": "us",
    "language": "en"
}

try:
    response = httpx.get(
        "https://real-time-product-search.p.rapidapi.com/product-reviews",
        headers=headers,
        params=params,
        timeout=60.0
    )

    print(f"Status: {response.status_code}")
    data = response.json()
    reviews = data.get("data", {}).get("reviews", [])
    print(f"Reviews found: {len(reviews)}")

    if reviews:
        print("\n✅ REVIEWS FOUND!")
        for r in reviews[:3]:
            print(f"\nRating: {r.get('rating')}")
            print(f"Source: {r.get('review_source', '')}")
            print(f"Title:  {r.get('review_title', '')}")
            print(f"Body:   {r.get('review_text', '')[:150]}")
    else:
        print("❌ No reviews")

except Exception as e:
    print(f"❌ Error: {e}")