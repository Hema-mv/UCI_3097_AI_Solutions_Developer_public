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

params = {
    "q": "linen shower curtain etsy handmade",
    "country": "us",
    "language": "en",
    "limit": "3"
}

response = httpx.get(
    "https://real-time-product-search.p.rapidapi.com/search",
    headers=headers,
    params=params,
    timeout=60.0
)

data = response.json()
products = data.get("data", {}).get("products", [])

for p in products:
    print(f"\nTitle:  {p.get('product_title', '')[:60]}")
    print(f"Store:  {p.get('store_name', '')}")
    print(f"Price:  {p.get('price', '')}")
    print(f"Rating: {p.get('product_rating', '')}")
    print(f"Photos: {p.get('product_photos', [])}")