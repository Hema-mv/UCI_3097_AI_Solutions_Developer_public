import pandas as pd
import re

def load_reviews(csv_path: str, max_rows: int = 500) -> list[dict]:
    """
    Load reviews from a CSV file and return a clean list of dicts.
    """
    df = pd.read_csv(csv_path, nrows=max_rows)

    print("CSV columns:", df.columns.tolist())

    reviews = []
    for _, row in df.iterrows():
        rating = row.get("Score", row.get("rating", 3))
        title  = str(row.get("Summary", row.get("title", "")))
        body   = str(row.get("Text", row.get("body", "")))

        cleaned_body = clean_text(body)

        if len(cleaned_body) < 20:
            continue

        reviews.append({
            "rating": float(rating),
            "title": title,
            "body": cleaned_body,
            "full_text": f"{title}. {cleaned_body}"
        })

    print(f"Loaded {len(reviews)} reviews")
    return reviews


def clean_text(text: str) -> str:
    """Remove HTML tags, URLs, and extra whitespace."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()