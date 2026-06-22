from scrapers.walmart import scrape_walmart
from services.embeddings import embed_texts
from services.vector_store import store_reviews, search_reviews
from services.llm import generate_insight

print("Step 1: Fetching reviews from Walmart...")
url = "https://www.walmart.com/ip/Neutrogena-Hydro-Boost-Water-Gel-Face-Moisturizer-Lotion-with-Hyaluronic-Acid-1-7-oz/40488263"
reviews = scrape_walmart(url, max_reviews=30)
print(f"Fetched {len(reviews)} reviews")

print("\nStep 2: Storing in ChromaDB...")
store_reviews(reviews)
print("Stored successfully!")

print("\nStep 3: Searching for complaints...")
results = search_reviews("problem issue disappointed bad", n_results=5)
for i, r in enumerate(results, 1):
    print(f"\nResult {i}: {r[:100]}")

print("\nStep 4: Generating AI insight...")
insight = generate_insight("complaints", results)
print("\nAI Complaints Analysis:")
print(insight)