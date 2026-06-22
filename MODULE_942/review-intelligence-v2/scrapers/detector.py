from urllib.parse import urlparse

def detect_platform(url: str) -> str:
    """Detect which marketplace the URL belongs to."""
    domain = urlparse(url).netloc.lower()

    if "walmart.com" in domain:
        return "walmart"
    elif "etsy.com" in domain:
        return "etsy"
    elif "amazon.com" in domain or "amazon.in" in domain:
        return "amazon"
    else:
        raise ValueError(f"Unsupported platform. Please use Walmart, Etsy, or Amazon URLs.")

def extract_walmart_id(url: str) -> str:
    """Extract the item ID from a Walmart URL."""
    path = urlparse(url).path
    parts = path.strip("/").split("/")
    for part in reversed(parts):
        if part.isdigit():
            return part
    raise ValueError("Could not find Walmart item ID in URL.")