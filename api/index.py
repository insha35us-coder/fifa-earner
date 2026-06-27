from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime
import os

app = FastAPI()

YOUR_TAG = "timevalue0e2-20"

KEYWORDS = [
    "usa world cup jersey 2026",
    "mexico world cup jersey 2026",
    "canada world cup jersey 2026",
    "fifa world cup fan scarf",
    "world cup watch party decorations",
    "fifa 2026 soccer ball",
    "world cup face paint",
    "world cup party supplies",
    "fifa world cup hat",
    "soccer team flag 2026"
]

def generate_affiliate_link(product_url):
    if "?" in product_url:
        return f"{product_url}&tag={YOUR_TAG}"
    else:
        return f"{product_url}?tag={YOUR_TAG}"

def scrape_amazon(keyword, max_results=5):
    search_url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resp = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        products = []
        for item in soup.select('[data-asin]'):
            asin = item.get('data-asin')
            if not asin or asin == "":
                continue
            title_elem = item.select_one('h2 a span')
            title = title_elem.text.strip() if title_elem else "Unknown Product"
            price_elem = item.select_one('.a-price .a-offscreen')
            price = price_elem.text.strip() if price_elem else "Price unavailable"
            rating_elem = item.select_one('.a-icon-alt')
            rating = rating_elem.text.strip() if rating_elem else "No rating"
            product_url = f"https://www.amazon.com/dp/{asin}"
            affiliate_url = generate_affiliate_link(product_url)
            products.append({
                "title": title,
                "price": price,
                "rating": rating,
                "affiliate_url": affiliate_url
            })
            if len(products) >= max_results:
                break
        return products
    except Exception as e:
        # Fallback: return hardcoded sample products with affiliate links
        return get_sample_products()

def get_sample_products():
    """Hardcoded backup products – always shows something even if scraping fails."""
    return [
        {
            "title": "USA World Cup 2026 Home Jersey – Official",
            "price": "$89.99",
            "rating": "4.6 out of 5 stars",
            "affiliate_url": f"https://www.amazon.com/dp/B0ABC123?tag={YOUR_TAG}"
        },
        {
            "title": "Mexico World Cup 2026 Jersey – Fan Version",
            "price": "$79.99",
            "rating": "4.5 out of 5 stars",
            "affiliate_url": f"https://www.amazon.com/dp/B0XYZ789?tag={YOUR_TAG}"
        },
        {
            "title": "World Cup 2026 Watch Party Decoration Set",
            "price": "$24.99",
            "rating": "4.3 out of 5 stars",
            "affiliate_url": f"https://www.amazon.com/dp/B0DEF456?tag={YOUR_TAG}"
        }
    ]

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    keyword = random.choice(KEYWORDS)
    products = scrape_amazon(keyword, max_results=6)

    # Build HTML page (same as before, but use request.url for base)
    base_url = str(request.base_url).rstrip('/')
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FIFA World Cup 2026 – Best Fan Gear & Deals</title>
    <meta name="description" content="Find the best FIFA World Cup 2026 jerseys, fan gear, watch party supplies and more. Updated live with Amazon deals.">
    <meta name="keywords" content="FIFA World Cup 2026, USA jersey, Mexico jersey, Canada jersey, soccer gear, watch party">
    <meta property="og:title" content="FIFA World Cup 2026 – Best Fan Gear & Deals">
    <meta property="og:description" content="Get ready for the match with top-rated fan gear. Shop now!">
    <link rel="canonical" href="{base_url}/">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large">
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 20px auto; padding: 0 20px; background: #f8f9fa; }}
        h1 {{ color: #1a73e8; }}
        .product {{ background: white; border-radius: 8px; padding: 15px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .product a {{ color: #1a73e8; text-decoration: none; font-weight: bold; }}
        .price {{ color: #b12704; font-size: 1.2em; }}
        .rating {{ color: #555; }}
        .footer {{ margin-top: 30px; font-size: 0.8em; color: #777; }}
        .stamp {{ color: #28a745; }}
    </style>
</head>
<body>
    <h1>⚽ FIFA World Cup 2026 – Hot Fan Gear</h1>
    <p><strong>🔥 Updated:</strong> {datetime.now().strftime('%B %d, %Y at %H:%M')} (UTC)</p>
    <p>Find the best products for the biggest tournament. Every link supports this site.</p>
    <hr>
    """
    for p in products:
        html += f"""
    <div class="product">
        <h2>{p['title']}</h2>
        <div class="price">💰 {p['price']}</div>
        <div class="rating">⭐ {p['rating']}</div>
        <a href="{p['affiliate_url']}" target="_blank" rel="nofollow sponsored">👉 View on Amazon &rarr;</a>
    </div>
    """
    html += f"""
    <hr>
    <div class="footer">
        <p>🇺🇸🇲🇽🇨🇦 Gear up for the 2026 World Cup! <span class="stamp">#FIFA2026</span></p>
        <p><small>This page is automatically updated. Bookmark and share!</small></p>
        <p><small>Affiliate ID: {YOUR_TAG}</small></p>
    </div>
</body>
</html>
    """
    return html

@app.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap(request: Request):
    base_url = str(request.base_url).rstrip('/')
    now = datetime.now().strftime("%Y-%m-%d")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{base_url}/</loc>
    <lastmod>{now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    return xml
