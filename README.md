# News Sentiment Analysis Dashboard

A Streamlit-based dashboard that fetches news articles, performs sentiment analysis, and visualizes the results with word clouds and sentiment metrics.

## Features

- 📰 **News Fetching**: Fetch news from various categories (Business, Technology, Sports, Health, Politics, Entertainment)
- 📅 **Date Range Selection**: Filter news by custom date range
- 🧠 **Sentiment Analysis**: Analyze news sentiment using TextBlob (Positive, Negative, Neutral)
- ☁️ **Word Cloud**: Visualize frequently used words in news articles
- 📊 **Sentiment Metrics**: Display summary statistics for sentiment distribution
- 🔍 **Filtering**: Filter news by sentiment type
- 💾 **SQLite Database**: Store articles and sentiment analysis for historical tracking
- 📈 **Search History**: Track and view previous searches
- ⚙️ **User Preferences**: Save and restore user settings

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd news-sentiment-dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up API key:
   - Get an API key from [Bing News Search API](https://www.microsoft.com/en-us/bing/apis/bing-news-search-api)
   - Copy `.env.example` to `.env`
   - Add your API key to `.env`

5. Initialize the database:
```bash
python src/database/init_db.py
```

6. Run the app:
```bash
streamlit run app.py
```

## Project Structure

```
news-sentiment-dashboard/
├── .gitignore
├── README.md
├── requirements.txt
├── .env.example
├── config.py
├── app.py
├── src/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── news_fetcher.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── sentiment.py
│   │   └── helpers.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── categories.py
│   └── database/
│       ├── __init__.py
│       ├── models.py
│       ├── utils.py
│       └── init_db.py
├── tests/
│   ├── __init__.py
│   ├── test_news_fetcher.py
│   ├── test_sentiment.py
│   └── test_database.py
├── docs/
│   └── API_SETUP.md
└── assets/
    └── .gitkeep
```

## API Configuration

### Bing News Search API

1. Go to [Azure Portal](https://portal.azure.com/)
2. Create a Bing News Search resource
3. Copy the API key
4. Add it to your `.env` file

Free tier: 1,000 transactions per month

## Usage

1. Select a news category from the dropdown
2. Choose a date range (default: last 7 days)
3. Click "Refresh News" to fetch articles
4. View sentiment analysis summary and word cloud
5. Filter articles by sentiment type
6. Click on article links to read full stories

## Dependencies

- streamlit
- pandas
- textblob
- wordcloud
- matplotlib
- requests
- python-dotenv

## License

MIT License
