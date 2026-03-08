"""
api/news.py - FAST VERSION with caching (10 min cache)
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY  = os.getenv("NEWS_API_KEY", "")
BASE_URL = "https://newsapi.org/v2"

_cache = {}
CACHE_SECONDS = 600   # 10 minutes


def get_top_headlines(category: str = "technology", country: str = "in", count: int = 5) -> list:
    if not API_KEY:
        return [{"error": "NEWS_API_KEY not set in .env"}]

    cache_key = f"{category}_{country}_{count}"
    if cache_key in _cache:
        ts, data = _cache[cache_key]
        if time.time() - ts < CACHE_SECONDS:
            print(f"[News] Returning cached headlines for {category}")
            return data

    try:
        resp = requests.get(
            f"{BASE_URL}/top-headlines",
            params={"apiKey": API_KEY, "category": category, "country": country, "pageSize": count},
            timeout=6
        )
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        data = [
            {
                "title":       a.get("title", "No title"),
                "source":      a.get("source", {}).get("name", "Unknown"),
                "description": a.get("description", ""),
                "url":         a.get("url", ""),
            }
            for a in articles
        ]
        _cache[cache_key] = (time.time(), data)
        return data
    except Exception as e:
        return [{"error": f"News fetch failed: {e}"}]


def format_news(category: str = "technology", count: int = 5) -> str:
    articles = get_top_headlines(category=category, count=count)
    if not articles:
        return "No news found."
    if "error" in articles[0]:
        return f"News error: {articles[0]['error']}"
    lines = [f"Latest {category.capitalize()} News:\n"]
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. [{a['source']}] {a['title']}")
        if a.get("description"):
            lines.append(f"   {a['description'][:100]}...")
        lines.append("")
    return "\n".join(lines)