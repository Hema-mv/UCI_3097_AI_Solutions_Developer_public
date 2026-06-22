import httpx

# Try old key first
ETSY_API_KEY = "mci82rm3fue6d6qal9m34ssi"

listing_id = "1797455914"

response = httpx.get(
    f"https://openapi.etsy.com/v3/application/listings/{listing_id}/reviews",
    headers={"x-api-key": ETSY_API_KEY},
    params={"limit": 10, "offset": 0},
    timeout=30.0
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:1000]}")