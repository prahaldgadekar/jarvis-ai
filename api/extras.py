"""
api/extras.py
Extra APIs for JARVIS - Wikipedia, Crypto, Jokes, NASA, IP info.
All either free or no-key-required.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN       = os.getenv("GITHUB_TOKEN", "")
EXCHANGE_RATE_KEY  = os.getenv("EXCHANGE_RATE_KEY", "")
NASA_KEY           = os.getenv("NASA_KEY", "DEMO_KEY")  # DEMO_KEY works without signup


# ── Wikipedia ─────────────────────────────────────────────────
def search_wikipedia(query: str) -> str:
    """Search Wikipedia and return a short summary. No API key needed."""
    try:
        resp = requests.get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_"),
            timeout=8,
            headers={"User-Agent": "JARVIS/1.0"}
        )
        if resp.status_code == 200:
            data = resp.json()
            title   = data.get("title", "")
            extract = data.get("extract", "")
            if extract:
                # Return first 2 sentences only
                sentences = extract.split(". ")
                short = ". ".join(sentences[:2]) + "."
                return f"{title}: {short}"
            return "No summary found."
        return f"Wikipedia: page not found for '{query}'."
    except Exception as e:
        return f"Wikipedia error: {e}"


# ── Crypto Prices ─────────────────────────────────────────────
def get_crypto_price(coin: str = "bitcoin") -> str:
    """Get current crypto price from CoinGecko. No API key needed."""
    coin_map = {
        "bitcoin": "bitcoin", "btc": "bitcoin",
        "ethereum": "ethereum", "eth": "ethereum",
        "dogecoin": "dogecoin", "doge": "dogecoin",
        "solana": "solana", "sol": "solana",
        "bnb": "binancecoin", "xrp": "ripple",
    }
    coin_id = coin_map.get(coin.lower(), coin.lower())
    try:
        resp = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd,inr",
            timeout=8
        )
        data = resp.json()
        if coin_id in data:
            usd = data[coin_id].get("usd", "N/A")
            inr = data[coin_id].get("inr", "N/A")
            return f"{coin.capitalize()}: USD {usd:,}  |  INR {inr:,}"
        return f"Coin '{coin}' not found."
    except Exception as e:
        return f"Crypto error: {e}"


def get_top_crypto(limit: int = 5) -> str:
    """Get top N cryptocurrencies by market cap."""
    try:
        resp = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1",
            timeout=8
        )
        coins = resp.json()
        lines = ["Top Crypto Prices:\n"]
        for i, c in enumerate(coins, 1):
            lines.append(f"  {i}. {c['name']} ({c['symbol'].upper()}): USD {c['current_price']:,}  change: {c['price_change_percentage_24h']:.1f}%")
        return "\n".join(lines)
    except Exception as e:
        return f"Crypto error: {e}"


# ── Joke ──────────────────────────────────────────────────────
def get_joke(category: str = "programming") -> str:
    """Get a random joke. No API key needed."""
    try:
        resp = requests.get(
            f"https://v2.jokeapi.dev/joke/{category}?blacklistFlags=nsfw,racist,sexist",
            timeout=8
        )
        data = resp.json()
        if data.get("type") == "single":
            return data.get("joke", "No joke found.")
        if data.get("type") == "twopart":
            return data.get("setup", "") + "\n" + data.get("delivery", "")
        return "Could not get a joke right now."
    except Exception as e:
        return f"Joke error: {e}"


# ── NASA Picture of the Day ───────────────────────────────────
def get_nasa_apod() -> str:
    """Get NASA Astronomy Picture of the Day. Use DEMO_KEY or your own key."""
    try:
        resp = requests.get(
            f"https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}",
            timeout=8
        )
        data = resp.json()
        title       = data.get("title", "Unknown")
        explanation = data.get("explanation", "")
        date        = data.get("date", "")
        url         = data.get("url", "")
        short = ". ".join(explanation.split(". ")[:2]) + "."
        return f"NASA APOD - {date}\nTitle: {title}\n{short}\nLink: {url}"
    except Exception as e:
        return f"NASA error: {e}"


# ── IP and Location ───────────────────────────────────────────
def get_my_ip_info() -> str:
    """Get your public IP and location info. No key needed."""
    try:
        resp = requests.get("https://ipapi.co/json/", timeout=6)
        data = resp.json()
        ip      = data.get("ip", "N/A")
        city    = data.get("city", "N/A")
        region  = data.get("region", "N/A")
        country = data.get("country_name", "N/A")
        isp     = data.get("org", "N/A")
        return f"Your IP: {ip}\nLocation: {city}, {region}, {country}\nISP: {isp}"
    except Exception as e:
        return f"IP info error: {e}"


# ── Currency Exchange ─────────────────────────────────────────
def get_exchange_rate(from_cur: str = "USD", to_cur: str = "INR") -> str:
    """Get exchange rate. Uses free exchangerate-api (no key needed for basic)."""
    try:
        resp = requests.get(
            f"https://api.exchangerate-api.com/v4/latest/{from_cur.upper()}",
            timeout=8
        )
        data = resp.json()
        rates = data.get("rates", {})
        rate  = rates.get(to_cur.upper())
        if rate:
            return f"1 {from_cur.upper()} = {rate} {to_cur.upper()}"
        return f"Currency {to_cur} not found."
    except Exception as e:
        return f"Exchange rate error: {e}"


# ── GitHub ────────────────────────────────────────────────────
def get_github_profile(username: str) -> str:
    """Get GitHub user profile info."""
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    try:
        resp = requests.get(
            f"https://api.github.com/users/{username}",
            headers=headers, timeout=8
        )
        data = resp.json()
        if resp.status_code == 404:
            return f"GitHub user '{username}' not found."
        return (
            f"GitHub: {data.get('name', username)}\n"
            f"  Repos  : {data.get('public_repos', 0)}\n"
            f"  Followers: {data.get('followers', 0)}\n"
            f"  Bio    : {data.get('bio', 'N/A')}"
        )
    except Exception as e:
        return f"GitHub error: {e}"