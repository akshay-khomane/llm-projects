import feedparser
import json
import os
from datetime import datetime
from urllib.parse import quote

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_DIR, exist_ok=True)

ARTICLES_FILE = os.path.join(DATA_DIR, "articles.json")

def scrape_google_news_rss(query="technology", max_articles=10):
    encoded_query = quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:max_articles]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary,
            "source": entry.get("source", {}).get("title", "Unknown"),
            "scraped_at": datetime.utcnow().isoformat()
        })
    return articles


def save_articles(articles):
    for article in articles:
        article["scraped_at"] = datetime.now().isoformat()
    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "latest news"
    articles = scrape_google_news_rss(query=topic, max_articles=10)
    save_articles(articles)
