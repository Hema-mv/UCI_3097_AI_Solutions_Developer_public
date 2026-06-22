import time
from playwright.sync_api import sync_playwright

def scrape_etsy(url: str, max_reviews: int = 100) -> list[dict]:
    """
    Scrape Etsy reviews using Playwright.
    Etsy loads reviews dynamically so we need a real browser.
    """
    listing_id = extract_etsy_id(url)
    print(f"Etsy listing ID: {listing_id}")

    reviews = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        print("Opening Etsy page...")
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        # Close any popups
        try:
            page.click("button[data-gdpr-single-choice-accept]", timeout=3000)
            print("Closed GDPR popup")
        except:
            pass

        try:
            page.click("button[aria-label='Close']", timeout=3000)
            print("Closed popup")
        except:
            pass

        # Scroll to reviews section
        print("Scrolling to reviews...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.6)")
        page.wait_for_timeout(2000)

        # Look for reviews section
        page_num = 1
        while len(reviews) < max_reviews:
            print(f"Scraping page {page_num}...")

            # Wait for reviews to load
            page.wait_for_timeout(2000)

            # Extract reviews from current page
            review_elements = page.query_selector_all("[data-reviews-list] li")

            if not review_elements:
                # Try alternative selector
                review_elements = page.query_selector_all(".wt-grid__item-xs-12 .wt-text-body-01")

            if not review_elements:
                review_elements = page.query_selector_all("[class*='review']")

            print(f"Found {len(review_elements)} review elements")

            for element in review_elements:
                try:
                    # Get review text
                    body = element.inner_text().strip()

                    # Get rating
                    rating_el = element.query_selector("[aria-label*='star']")
                    if rating_el:
                        aria = rating_el.get_attribute("aria-label") or "5"
                        rating = float(''.join(filter(str.isdigit, aria.split()[0])) or "5")
                    else:
                        rating = 5.0

                    if len(body) > 20:
                        reviews.append({
                            "platform": "etsy",
                            "rating": rating,
                            "title": "",
                            "body": body,
                            "full_text": body,
                        })
                except:
                    continue

            # Try to go to next page
            try:
                next_btn = page.query_selector("a[aria-label='Go to next page']") or \
                           page.query_selector("a[rel='next']") or \
                           page.query_selector("button[aria-label='Next page']")

                if next_btn and len(reviews) < max_reviews:
                    next_btn.click()
                    page.wait_for_timeout(3000)
                    page_num += 1
                else:
                    print("No more pages")
                    break
            except:
                print("Could not find next page button")
                break

        browser.close()

    # Remove duplicates
    seen = set()
    unique_reviews = []
    for r in reviews:
        if r["body"] not in seen and len(r["body"]) > 20:
            seen.add(r["body"])
            unique_reviews.append(r)

    print(f"Total unique reviews: {len(unique_reviews)}")
    return unique_reviews[:max_reviews]


def extract_etsy_id(url: str) -> str:
    """Extract listing ID from Etsy URL."""
    # Etsy URLs: https://www.etsy.com/listing/1654494480/product-name
    parts = url.split("/listing/")
    if len(parts) > 1:
        listing_id = parts[1].split("/")[0]
        return listing_id
    raise ValueError("Could not find Etsy listing ID in URL")