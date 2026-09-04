"""
Live Gold/Silver Rate Fetcher for Jewellery Website Widget
Uses GoldAPI.io free tier (sign up at goldapi.io for your key)
"""

import requests

# Get your free API key at https://www.goldapi.io/ (no card required)
API_KEY = "goldapi-2f03015577e8ab9e3fde3348729c40db-io"

BASE_URL = "https://www.goldapi.io/api"


def get_metal_price(metal_symbol: str, currency: str = "INR") -> dict:
    """
    metal_symbol options: 'XAU' (gold), 'XAG' (silver), 'XPT' (platinum), 'XPD' (palladium)
    currency: any supported currency code, e.g. 'INR', 'USD'
    """
    url = f"{BASE_URL}/{metal_symbol}/{currency}"
    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    return {
        "metal": data.get("metal"),
        "currency": data.get("currency"),
        "price_per_gram_24k": data.get("price_gram_24k"),
        "price_per_gram_22k": data.get("price_gram_22k"),
        "price_per_gram_18k": data.get("price_gram_18k"),
        "price_per_ounce": data.get("price"),
        "timestamp": data.get("timestamp"),
    }


def build_widget_data():
    """Fetch gold and silver prices for display on jewellery site."""
    gold = get_metal_price("XAU", "INR")
    silver = get_metal_price("XAG", "INR")

    return {
        "gold": gold,
        "silver": silver,
    }


if __name__ == "__main__":
    data = build_widget_data()
    print("Gold (per gram, 22K):", data["gold"]["price_per_gram_22k"], "INR")
    print("Silver (per gram):", data["silver"]["price_per_gram_24k"], "INR")