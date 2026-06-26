from scrapers.amazon import scrape_amazon
from services.vector_store import store_reviews, search_reviews
from services.llm import generate_insight

# Full URL with product name — gives better search results
url = "https://www.amazon.com/Amazon-Echo-Spot-2024-release/dp/B0BFC7WQ6R"

print("Step 1: Fetching Amazon reviews...")
reviews = scrape_amazon(url, max_reviews=10)
print(f"Fetched {len(reviews)} reviews ✅")

print("\nStep 2: Storing in ChromaDB...")
store_reviews(reviews)
print("Stored ✅")

print("\nStep 3: Generating complaints...")
results = search_reviews("problem issue bad disappointed", n_results=10)
insight = generate_insight("complaints", results)
print("\nAI Complaints:")
print(insight)