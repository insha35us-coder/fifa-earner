from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
import json
import os
from datetime import datetime
import random

app = FastAPI()

YOUR_TAG = "timevalue0e2-20"

def load_categories():
    try:
        path = os.path.join(os.path.dirname(__file__), "..", "products.json")
        with open(path, "r") as f:
            return json.load(f)
    except:
        return [{"category": "FIFA 2026 Gear", "keyword": "FIFA+World+Cup+2026", "image": "", "desc": "Shop now"}]

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    categories = load_categories()
    base = str(request.base_url).rstrip('/')
    
    # Shuffle to show different order for Google freshness
    random.shuffle(categories)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FIFA World Cup 2026 – Official Gear, Jerseys & Fan Deals</title>
    <meta name="description" content="Shop the best FIFA 2026 World Cup merchandise. USA, Mexico, Canada jerseys, official balls, Panini stickers, and watch party supplies. Updated daily.">
    <meta name="keywords" content="FIFA World Cup 2026, USA jersey, Mexico jersey, Canada jersey, World Cup ball, Panini stickers, fan gear, soccer deals">
    <link rel="canonical" href="{base}/">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow, max-snippet:-1">
    <meta property="og:title" content="FIFA World Cup 2026 – Official Fan Gear">
    <meta property="og:description" content="Find the best FIFA 2026 products. Live deals on Amazon.">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ text-align: center; color: #1a73e8; font-size: 2.5rem; margin-bottom: 5px; }}
        .sub {{ text-align: center; color: #555; margin-bottom: 20px; }}
        .updated {{ text-align: center; color: #28a745; font-weight: bold; margin-bottom: 30px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 25px; }}
        .card {{ background: white; border-radius: 12px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; transition: 0.3s; }}
        .card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); }}
        .card img {{ width: 100%; height: 180px; object-fit: contain; background: #f8f9fa; border-radius: 8px; }}
        .card h2 {{ font-size: 1.1rem; margin: 12px 0 5px; height: 40px; overflow: hidden; }}
        .card p {{ font-size: 0.9rem; color: #666; height: 40px; overflow: hidden; }}
        .btn {{ display: inline-block; background: #ff9900; color: #000; padding: 10px 20px; border-radius: 30px; text-decoration: none; font-weight: bold; margin-top: 10px; }}
        .btn:hover {{ background: #e68a00; }}
        .footer {{ text-align: center; margin-top: 40px; color: #777; border-top: 1px solid #ddd; padding-top: 20px; }}
        .hashtag {{ color: #1a73e8; }}
    </style>
</head>
<body>
<div class="container">
    <h1>⚽ FIFA World Cup 2026</h1>
    <div class="sub">🇺🇸 🇲🇽 🇨🇦 Official Fan Gear • Jerseys • Collectibles</div>
    <div class="updated">🔥 Live Deals – Updated {datetime.now().strftime('%B %d, %Y at %H:%M')} (UTC)</div>
    <div class="grid">
"""
    
    for cat in categories:
        link = f"https://www.amazon.com/s?k={cat['keyword']}&tag={YOUR_TAG}"
        img = cat.get('image', '')
        img_tag = f'<img src="{img}" alt="{cat["category"]}">' if img else '<div style="height:180px;background:#eee;display:flex;align-items:center;justify-content:center;border-radius:8px;">🛒</div>'
        html += f"""
        <div class="card">
            {img_tag}
            <h2>{cat['category']}</h2>
            <p>{cat.get('desc', '')}</p>
            <a href="{link}" target="_blank" rel="nofollow sponsored" class="btn">View on Amazon →</a>
        </div>
        """
    
    html += f"""
    </div>
    <div class="footer">
        <p><span class="hashtag">#FIFA2026</span> • <span class="hashtag">#WorldCup</span> • <span class="hashtag">#Soccer</span></p>
        <p><small>Your affiliate ID: {YOUR_TAG} • This page is indexed daily by Google.</small></p>
        <p><small>© 2026 • Made for fans worldwide</small></p>
    </div>
</div>
</body>
</html>
"""
    return html

@app.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap(request: Request):
    base = str(request.base_url).rstrip('/')
    now = datetime.now().strftime("%Y-%m-%d")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{base}/</loc><lastmod>{now}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>
</urlset>"""
