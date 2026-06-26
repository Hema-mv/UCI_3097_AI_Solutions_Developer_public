# test_walmart.py
from scrapers.walmart import scrape_walmart

url = "https://www.walmart.com/ip/Neutrogena-Hydro-Boost-Water-Gel-Face-Moisturizer-Lotion-with-Hyaluronic-Acid-1-7-oz/40488263"

# Simulate user setting slider to 30
reviews = scrape_walmart(url, max_reviews=30)

print(f"\nTotal reviews: {len(reviews)}")
for r in reviews[:3]:
    print(f"\nRating: {r['rating']}")
    print(f"Title:  {r['title']}")
    print(f"Body:   {r['body'][:150]}")
    print("---")