import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from .sources import SOURCES
import time

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def fetch_html(source):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(source['url'], timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select(source['selector'])

            results = []
            for item in items[:10]:
                title = item.get_text(strip=True)
                url = item.get("href", "")
                description = item.get("title", "") or title
                results.append({
                    "title": title,
                    "description": description,
                    "url": url,
                    "timestamp": datetime.utcnow().isoformat()
                })
            return results

        except Exception as e:
            print(f"[HTML Error] {source['url']} attempt {attempt} -> {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                return []


def fetch_rss(source):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            feed = feedparser.parse(source['url'])
            results = []
            for entry in feed.entries[:10]:
                results.append({
                    "title": getattr(entry, "title", ""),
                    "description": getattr(entry, "summary", ""),
                    "url": getattr(entry, "link", ""),
                    "timestamp": getattr(entry, "published", datetime.utcnow().isoformat())
                })
            return results
        except Exception as e:
            print(f"[RSS Error] {source['url']} attempt {attempt} -> {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                return []


def fetch_api(source):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(source['url'], params=source.get('params', {}), timeout=10)
            response.raise_for_status()
            data = response.json()
            results = []

            for article in data.get('articles', [])[:10]:
                results.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "url": article.get("url", ""),
                    "timestamp": article.get("publishedAt", datetime.utcnow().isoformat())
                })
            return results
        except Exception as e:
            print(f"[API Error] {source['url']} attempt {attempt} -> {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                return []


def fetch_all():
    all_data = {}
    for name, src in SOURCES.items():
        print(f"[Fetching] from {name}....")
        if src['type'] == 'html':
            all_data[name] = fetch_html(src)
        elif src['type'] == 'rss':
            all_data[name] = fetch_rss(src)
        elif src['type'] == 'api':
            all_data[name] = fetch_api(src)
        else:
            print(f"[Fetcher] Unknown source type: {src['type']}")
            all_data[name] = []
    return all_data


if __name__ == "__main__":
    results = fetch_all()
    for source, items in results.items():
        print(f"\n{source.upper()} - {len(items)} items")
        for i, item in enumerate(items, 1):
            print(f"  {i}. Title: {item['title']}, Desc: {item['description']}, URL: {item['url']}, Time: {item['timestamp']}")
