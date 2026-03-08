"""
api/news.py
-----------
Fetches latest news from NewsAPI.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY  = os.getenv("NEWS_API_KEY", "")
BASE_URL = "https://newsapi.org/v2"


def get_top_headlines(category: str = "technology", country: str = "in", count: int = 5) -> list:
    """
    Fetch top news headlines.
    
    category options: business, entertainment, general, health, science, sports, technology
    country: 'in' for India, 'us' for US, etc.
    """
    if not API_KEY:
        return [{"error": "NEWS_API_KEY not set in .env"}]

    try:
        resp = requests.get(
            f"{BASE_URL}/top-headlines",
            params={
                "apiKey":   API_KEY,
                "category": category,
                "country":  country,
                "pageSize": count,
            },
            timeout=10
        )
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        return [
            {
                "title":       a.get("title", "No title"),
                "source":      a.get("source", {}).get("name", "Unknown"),
                "description": a.get("description", ""),
                "url":         a.get("url", ""),
                "published":   a.get("publishedAt", "")[:10],
            }
            for a in articles
        ]
    except Exception as e:
        return [{"error": f"News fetch failed: {e}"}]


def format_news(category: str = "technology", count: int = 5) -> str:
    """Return formatted news headlines."""
    articles = get_top_headlines(category=category, count=count)
    if not articles:
        return "No news articles found."
    if "error" in articles[0]:
        return f"⚠️ News error: {articles[0]['error']}"

    lines = [f"📰 Latest {category.capitalize()} News:\n"]
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. [{a['source']}] {a['title']}")
        if a.get("description"):
            lines.append(f"   {a['description'][:120]}...")
        lines.append(f"   🔗 {a['url']}\n")

    return "\n".join(lines)


def search_news(query: str, count: int = 5) -> str:
    """Search news by keyword."""
    if not API_KEY:
        return "NEWS_API_KEY not set in .env"

    try:
        resp = requests.get(
            f"{BASE_URL}/everything",
            params={
                "apiKey":   API_KEY,
                "q":        query,
                "pageSize": count,
                "sortBy":   "publishedAt",
                "language": "en",
            },
            timeout=10
        )
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        if not articles:
            return f"No news found for '{query}'."

        lines = [f"🔍 News results for '{query}':\n"]
        for i, a in enumerate(articles, 1):
            lines.append(f"{i}. {a.get('title', 'No title')}")
            lines.append(f"   Source: {a.get('source', {}).get('name', 'Unknown')}")
            lines.append(f"   🔗 {a.get('url', '')}\n")
        return "\n".join(lines)
    except Exception as e:
        return f"Search failed: {e}"