import json
import os
import time
import subprocess
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the folder exists

ARTICLES_FILE = os.path.join(DATA_DIR, "articles.json")
SUMMARIES_FILE = os.path.join(DATA_DIR, "summaries.json")

def run_ollama(prompt, model="mistral"):
    try:
        # Runs the local Ollama model using subprocess and captures the output
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error running ollama: {e}"


def parse_ollama_output(output):
    # Extract summary, sentiment, and tags using regex, fallback to defaults if not found
    summary_match = re.search(r"Summary:(.*?)(?:Sentiment:|Overall Sentiment:|$)", output, re.DOTALL | re.IGNORECASE)
    sentiment_match = re.search(r"(?:Sentiment:|Overall Sentiment:)(.*?)(?:Tags:|Topic Tags:|Topic tags:|$)", output, re.DOTALL | re.IGNORECASE)
    tags_match = re.search(r"(?:Tags:|Topic Tags:|Topic tags:)(.*)", output, re.DOTALL | re.IGNORECASE)

    summary = summary_match.group(1).strip() if summary_match else output.strip()
    sentiment = sentiment_match.group(1).strip() if sentiment_match else "Unknown"
    tags = tags_match.group(1).strip() if tags_match else "None"

    # Only keep first line for sentiment and tags
    sentiment = sentiment.splitlines()[0] if sentiment else "Unknown"
    tags = tags.splitlines()[0] if tags else "None"

    # Standardize output
    return f"Summary: {summary}\nSentiment: {sentiment}\nTags: {tags}"


def summarize_article(article):
    prompt = f"""
        You are a news summarizer. Given the article below, provide:
        - A short 3-sentence summary
        - The overall sentiment (Positive, Negative, Neutral)
        - One or two topic tags

        Article:
        Title: {article['title']}
        Description: {article['summary']}
    """
    output = run_ollama(prompt)
    return parse_ollama_output(output)


def summarize_articles(input_file=ARTICLES_FILE, output_file=SUMMARIES_FILE):
    with open(input_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    summaries = []
    for i, article in enumerate(articles):
        print(f"Summarizing article {i+1}/{len(articles)}: {article['title'][:60]}...")
        summary = summarize_article(article)
        summaries.append({
            "title": article["title"],
            "url": article["link"],
            "published": article["published"],
            "summary": summary,
            "scraped_at": article["scraped_at"]
        })
        time.sleep(1)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    summarize_articles()
