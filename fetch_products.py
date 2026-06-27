import requests
import json
import re
import os

YOUR_TAG = "timevalue0e2-20"

# Using a free RSS-to-JSON proxy. This NEVER gets blocked by Amazon.
RSS_URL = "https://api.rss2json.com/v1/api.json?rss_url=https://www.amazon.com/gp/rss/bestsellers/sporting-goods/3412851"

def get_asin(url):
    match = re.search(r'/dp/([A-Z0-9]{10})', url)
    return match.group(1) if match else None

try:
    response = requests.get(RSS_URL, timeout=30)
    data = response.json()
    items = data.get('items', [])

    real_products = []
    for item in items[:20]:  # Get Top 20 best-sellers
        link = item.get('link', '')
        asin = get_asin(link)
        if not asin:
            continue

        title = item.get('title', 'Unknown Product')
        description = item.get('description', '')

        # Build the REAL Amazon image URL
        image_url = f"https://ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={asin}&Format=_SL250_&ID=AsinImage&MarketPlace=US&ServiceVersion=20070822&WS=1&tag={YOUR_TAG}"
        
        # Build the affiliate link
        affiliate_url = f"https://www.amazon.com/dp/{asin}?tag={YOUR_TAG}"

        # Try to grab price from description if available
        price_match = re.search(r'\$(\d+\.\d{2})', description)
        price = f"${price_match.group(1)}" if price_match else "See on Amazon"

        real_products.append({
            "title": title[:80],
            "asin": asin,
            "price": price,
            "image": image_url,
            "affiliate_url": affiliate_url,
            "description": description[:120].replace('\n', ' ')
        })

    # Write the real data to a JSON file
    with open('products.json', 'w') as f:
        json.dump(real_products, f, indent=2)

    print(f"✅ Successfully fetched {len(real_products)} real products!")

except Exception as e:
    print(f"⚠️ Error: {e}")
    # If it fails, we do NOT overwrite the existing products.json.
    # The old real data stays safe.
    pass
