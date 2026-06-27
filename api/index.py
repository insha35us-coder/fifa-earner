from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
import json
import os
from datetime import datetime

app = FastAPI()
YOUR_TAG = "timevalue0e2-20"

def load_products():
    try:
        # Read the file that GitHub Actions updates every hour
        path = os.path.join(os.path.dirname(__file__), "..", "products.json")
        with open(path, "r") as f:
            return json.load(f)
    except:
        # Ultimate fallback (if the Action hasn't run yet)
        return [{
            "title": "Loading Real Products...",
            "asin": "",
            "price": "",
            "image": "",
            "affiliate_url": "#",
            "description": "GitHub Action will fetch real items in 1 minute."
        }]

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    products = load_products()
    base = str(request.base_url).rstrip('/')
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 FIFA 2026 REAL Best Sellers - Live Amazon Data</title>
    <meta name="description" content="Live, real-time best-selling FIFA World Cup 2026 gear. Official jerseys, balls, and fan items updated hourly from Amazon.">
    <meta name="keywords" content="FIFA 2026 best sellers, USA jersey, Mexico jersey, Canada jersey, World Cup ball, fan gear">
    <link rel="canonical" href="{base}/">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow, max-snippet:-1">
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ text-align: center; color: #1a73e8; font-size: 2.5rem; }}
        .badge {{ background: #28a745; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.9rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-top: 20px; }}
        .card {{ background: white; border-radius: 12px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }}
        .card img {{ width: 100%; height: 200px; object-fit: contain; background: #fff; border-radius: 8px; }}
        .card h2 {{ font-size: 1rem; height: 40px; overflow: hidden; margin: 10px 0; }}
        .card .price {{ font-size: 1.3rem; color: #b12704; font-weight: bold; }}
        .btn {{ display: inline-block; background: #ff9900; color: #000; padding: 10px 25px; border-radius: 30px; text-decoration: none; font-weight: bold; }}
        .btn:hover {{ background: #e68a00; }}
        .footer {{ text-align: center; margin-top: 40px; color: #555; border-top: 1px solid #ddd; padding-top: 20px; }}
        .updated {{ text-align: center; margin: 10px 0; }}
    </style>
</head>
<body>
<div class="container">
    <h1>⚽ FIFA 2026 <span class="badge">REAL Best Sellers</span></h1>
    <p style="text-align:center;">🇺🇸 🇲🇽 🇨🇦 Actual products fans are buying right now</p>
    <div class="updated">🔄 Updated Hourly • {datetime.now().strftime('%B %d, %Y at %H:%M')} (UTC)</div>
    <div class="grid">
"""
    for p in products:
        if not p.get('asin'):
            continue
        img = p.get('image', '')
        img_tag = f'<img src="{img}" alt="{p["title"]}" loading="lazy">' if img else '<div style="height:200px;background:#eee;">No Image</div>'
        html += f"""
        <div class="card">
            {img_tag}
            <h2>{p.get('title', '')}</h2>
            <div class="price">{p.get('price', '')}</div>
            <p style="font-size:0.8rem; color:#555; height:40px; overflow:hidden;">{p.get('description', '')}</p>
            <a href="{p.get('affiliate_url', '#')}" target="_blank" rel="nofollow sponsored" class="btn">View on Amazon</a>
        </div>
        """
    html += f"""
    </div>
    <div class="footer">
        <p><strong>#FIFA2026 #WorldCup #Soccer</strong></p>
        <p>Affiliate ID: {YOUR_TAG} | Data sourced from Amazon Official Best Sellers</p>
        <p><small>© 2026 • Built for fans</small></p>
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
  <url><loc>{base}/</loc><lastmod>{now}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>
</urlset>"""
