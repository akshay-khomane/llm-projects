# News Insight Aggregator

A Streamlit-powered dashboard that scrapes the latest news on any topic, summarizes articles using a local LLM (via [Ollama](https://ollama.com/)), and provides sentiment and tag analysis for quick insights.

---

## Features

- **Topic-based News Scraping:** Enter any topic to fetch the latest news articles from Google News.
- **Automated Summarization:** Summarizes articles using a local LLM (default: Mistral via Ollama).
- **Sentiment & Tag Extraction:** Extracts sentiment and topic tags for each article.
- **Interactive Dashboard:** Browse, filter, and read summaries in a modern UI.

---
## Demo

<img width="2520" height="261" alt="Screenshot 2025-07-19 at 8 40 07 PM" src="https://github.com/user-attachments/assets/73a57c40-1cd6-48a4-83cc-89432de591f6" />

<img width="2549" height="1258" alt="Screenshot 2025-07-19 at 8 42 23 PM" src="https://github.com/user-attachments/assets/aa40f5f7-ab56-4526-bd3c-17b57b17e009" />



## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/news-insight-aggregator.git
cd news-insight-aggregator
```

### 2. Set Up a Python Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Set Up Ollama

This project uses [Ollama](https://ollama.com/) to run a local LLM for summarization.  
- **Install Ollama:** Follow instructions at [https://ollama.com/download](https://ollama.com/download)
- **Pull a Model:**  
  The default model is `mistral`. You can pull it with:
  ```bash
  ollama pull mistral
  ```
- **Test Ollama:**  
  Run `ollama run mistral "Say hello"` to verify your setup.

### 5. Run the Dashboard

```bash
streamlit run dashboard.py
```

- The app will open in your browser at `http://localhost:8501`.

---

## Usage

1. **Enter a Topic:** Type a topic (e.g., "AI", "Elections", "Economy") in the input box.
2. **Generate News Summary:** Click the button to scrape news and generate summaries.
3. **Browse Summaries:** View summarized articles, sentiment, tags, and links to full articles.

---

## Project Structure

```
news-insight-aggregator/
├── dashboard.py                # Main Streamlit dashboard
├── scraper/
│   └── google_news.py          # News scraping script
├── summarizer/
│   └── ollama_summarizer.py    # LLM-based summarizer (requires Ollama)
├── data/
│   ├── articles.json           # Scraped articles (auto-generated)
│   └── summaries.json          # Summaries (auto-generated)
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/) (for local LLM summarization)
- See `requirements.txt` for Python dependencies:
  ```
  streamlit
  pandas
  feedparser
  ```

---

## Troubleshooting

- **No Summaries Found:** Ensure the scraper and summarizer scripts run without errors.
- **Ollama/Model Issues:** Make sure Ollama is running and the model (default: `mistral`) is available.
- **Permission Errors:** Make sure you have read/write access to the `data/` directory.

---

## Contributing

Pull requests and issues are welcome! Please open an issue to discuss your ideas or report bugs.

---

## License

[MIT](LICENSE)

---

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Ollama](https://ollama.com/)
- News data via Google News RSS

---

**Happy summarizing!** 
