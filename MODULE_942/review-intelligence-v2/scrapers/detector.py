from urllib.parse import urlparse, parse_qs
import re

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

def extract_amazon_asin(url: str) -> str:
    """
    Extract ASIN from Amazon URL.
    
    Handles these formats:
    - https://www.amazon.com/dp/B08N5WRWNW
    - https://www.amazon.com/product-name/dp/B08N5WRWNW
    - https://www.amazon.com/dp/B08N5WRWNW?ref=...
    - https://www.amazon.in/dp/B08N5WRWNW
    """
    import re
    path = urlparse(url).path

    # Look for /dp/ASIN pattern
    match = re.search(r'/dp/([A-Z0-9]{10})', path)
    if match:
        return match.group(1)

    # Look for /gp/product/ASIN pattern
    match = re.search(r'/gp/product/([A-Z0-9]{10})', path)
    if match:
        return match.group(1)

    raise ValueError(
        f"Could not find Amazon ASIN in URL: {url}\n"
        f"Make sure this is a valid Amazon product URL."
    )

def detect_platform(url: str) -> str:
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
    """
    Extract item ID from ANY Walmart URL format.
    
    Handles all these formats:
    - https://www.walmart.com/ip/product-name/765224053
    - https://www.walmart.com/ip/765224053
    - https://www.walmart.com/ip/product-name/5344517922?classType=VARIANT
    - https://www.walmart.com/ip/product/123?adsRedirect=true
    """
    # Remove query parameters and get just the path
    parsed = urlparse(url)
    path = parsed.path

    # Method 1: Look for /ip/ in path and get the number after it
    # Pattern: /ip/anything/NUMBER or /ip/NUMBER
    ip_match = re.search(r'/ip/(?:[^/]+/)?(\d+)', path)
    if ip_match:
        return ip_match.group(1)

    # Method 2: Find any long number in the path (Walmart IDs are 6-10 digits)
    numbers = re.findall(r'\d{6,10}', path)
    if numbers:
        return numbers[-1]  # Usually the last number is the item ID

    raise ValueError(
        f"Could not find Walmart item ID in URL: {url}\n"
        f"Please make sure this is a valid Walmart product URL."
    )