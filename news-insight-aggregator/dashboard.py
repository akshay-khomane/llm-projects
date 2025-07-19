import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
import subprocess

DATA_DIR = "data"
ARTICLES_FILE = os.path.join(DATA_DIR, "articles.json")
SUMMARIES_FILE = os.path.join(DATA_DIR, "summaries.json")

# Helper to get absolute path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Run the scraper
def run_scraper(topic):
    scraper_path = os.path.join(BASE_DIR, "scraper", "google_news.py")
    with st.spinner(f"🔄 Scraping news for topic: **{topic}** ..."):
        try:
            result = subprocess.run(["python3", scraper_path, topic], capture_output=True, text=True)
            st.code(result.stdout)
            if result.returncode != 0:
                st.error(f"Scraper failed: {result.stderr}")
            else:
                st.success("Scraping completed successfully.")
        except Exception as e:
            st.error(f"Error running scraper: {e}")

# Run the summarizer
def run_summarizer():
    summarizer_path = os.path.join(BASE_DIR, "summarizer", "ollama_summarizer.py")
    with st.spinner("🧠 Summarizing articles..."):
        try:
            result = subprocess.run(["python3", summarizer_path], capture_output=True, text=True)
            st.code(result.stdout)
            if result.returncode != 0:
                st.error(f"Summarizer failed: {result.stderr}")
            else:
                st.success("Summarization completed successfully.")
        except Exception as e:
            st.error(f"Error running summarizer: {e}")

@st.cache_data
def load_summaries():
    try:
        with open(SUMMARIES_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if not isinstance(raw, list):
            st.error("Summaries file format is invalid (expected a list).")
            return pd.DataFrame()
    except FileNotFoundError:
        st.warning("No summaries file found. Please generate news summaries first.")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        st.error(f"Summaries file is corrupted: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Failed to load summaries: {e}")
        return pd.DataFrame()

    summaries = []
    for article in raw:
        lines = article.get("summary", "").splitlines()
        summary_text = "\n".join([l for l in lines if not (l.lower().startswith("sentiment") or l.lower().startswith("overall sentiment") or l.lower().startswith("tags") or l.lower().startswith("topic tags"))])
        # Extract sentiment (Sentiment: or Overall Sentiment:)
        sentiment = next((l.split(":", 1)[1].strip() for l in lines if l.lower().startswith("sentiment") or l.lower().startswith("overall sentiment")), "Unknown")
        # Extract tags (Tags:, Topic Tags:, or Topic tags:)
        tags = next((l.split(":", 1)[1].strip() for l in lines if l.lower().startswith("tags") or l.lower().startswith("topic tags")), "None")

        # No sentiment filtering; show all articles
        summaries.append({
            "Title": article.get("title", "No Title"),
            "URL": article.get("url", ""),
            "Published": article.get("published", ""),
            "Summary": summary_text.strip(),
            "Sentiment": sentiment.title(),
            "Tags": tags,
            "Scraped At": article.get("scraped_at", "")
        })

    if not summaries:
        return pd.DataFrame()
    return pd.DataFrame(summaries)

# --- Streamlit UI ---
st.set_page_config(page_title="News Insight Dashboard", layout="wide")
st.title("News Insight Generator")

# --- Step 1: Topic Input ---
topic = st.text_input("Enter a topic (e.g., AI, Elections, Economy):", value="latest news")

if st.button("Generate News Summary"):
    run_scraper(topic)
    run_summarizer()
    # Optionally clear cache so new summaries are loaded
    load_summaries.clear()

# --- Step 2: Show Summaries ---
if os.path.exists(SUMMARIES_FILE):
    df = load_summaries()

    if df.empty:
        st.warning("No summaries found with positive or negative sentiment.")
    else:
        st.markdown(f"### Showing {len(df)} summarized articles")

        for _, row in df.iterrows():
            with st.expander(f"{row['Title']} ({row['Sentiment']})"):
                st.markdown(f"**Published**: {row['Published']}")
                st.markdown(f"**Tags**: {row['Tags']}")
                st.markdown(f"**Summary:**\n{row['Summary']}")
                st.markdown(f"[Read Full Article]({row['URL']})")
else:
    st.info("👆 Enter a topic and click 'Generate News Summary' to begin.")
