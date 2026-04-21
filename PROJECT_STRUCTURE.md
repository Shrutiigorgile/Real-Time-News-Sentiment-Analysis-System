# Project Structure

```
news-sentiment-dashboard/
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment variables template
├── README.md                   # Project documentation
├── PROJECT_STRUCTURE.md        # This file
├── requirements.txt            # Python dependencies
├── config.py                   # Configuration class with environment variables
│
├── app.py                      # Main Streamlit application (to be created)
├── app (1).py                  # Old app file (to be replaced)
├── news_api.py                 # Old API file (to be removed)
│
├── src/                        # Source code directory
│   ├── __init__.py
│   │
│   ├── api/                    # API integration module
│   │   ├── __init__.py
│   │   └── news_fetcher.py     # News fetching logic (Bing, NewsAPI, GNews)
│   │
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── sentiment.py        # Sentiment analysis functions
│   │   └── helpers.py          # Helper functions for data processing
│   │
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   └── categories.py       # Category definitions and mappings
│   │
│   └── database/               # Database module
│       ├── __init__.py
│       ├── models.py           # Database models and operations
│       ├── utils.py            # Database utility managers
│       └── init_db.py          # Database initialization script
│
├── tests/                      # Test directory
│   ├── __init__.py
│   ├── test_sentiment.py       # Sentiment analysis tests
│   └── test_database.py        # Database operations tests
│
├── docs/                       # Documentation
│   ├── API_SETUP.md            # API setup guide
│   └── DATABASE.md             # Database documentation
│
└── assets/                     # Static assets
    └── .gitkeep
```

## File Descriptions

### Root Files

- **.gitignore**: Specifies files to ignore in Git (Python cache, env files, IDE files)
- **.env.example**: Template for environment variables (API keys)
- **README.md**: Project overview, installation, and usage instructions
- **requirements.txt**: Python package dependencies
- **config.py**: Configuration class with API keys, endpoints, and settings

### Source Code (src/)

**api/news_fetcher.py**: Handles news fetching from multiple APIs
- `NewsFetcher`: Base class for news fetching
- `BingNewsFetcher`: Bing News Search API implementation
- `NewsAPIFetcher`: NewsAPI implementation
- `GNewsFetcher`: GNews API implementation
- `get_news_fetcher()`: Factory function to get appropriate fetcher

**utils/sentiment.py**: Sentiment analysis utilities
- `get_sentiment()`: Get sentiment polarity score
- `get_sentiment_label()`: Convert score to label (Positive/Negative/Neutral)
- `analyze_article()`: Analyze sentiment of an article

**utils/helpers.py**: Helper functions
- `articles_to_dataframe()`: Convert articles to pandas DataFrame
- `extract_text()`: Extract text for word cloud
- `get_current_timestamp()`: Get formatted timestamp
- `format_date()`: Format date strings

**models/categories.py**: Category management
- `get_categories()`: Get available categories
- `get_category_query()`: Get API query for category
- `is_valid_category()`: Validate category

**database/models.py**: Database models and operations
- `Database`: Main database class with CRUD operations
- `insert_article()`: Insert or update articles
- `insert_sentiment()`: Store sentiment analysis results
- `get_articles_by_category()`: Fetch articles by category
- `get_articles_by_date_range()`: Fetch articles by date range
- `get_sentiment_summary()`: Get sentiment statistics
- `save_preference()`: Save user preferences
- `get_preference()`: Retrieve user preferences
- `log_search()`: Log search history
- `delete_old_articles()`: Cleanup old articles
- `get_statistics()`: Get database statistics

**database/utils.py**: Database utility managers
- `ArticleManager`: High-level article operations
- `PreferenceManager`: User preference management
- `SearchHistoryManager`: Search history tracking

**database/init_db.py**: Database initialization script
- Creates all tables and indexes
- Can be run standalone to initialize database

### Tests (tests/)

- **test_sentiment.py**: Unit tests for sentiment analysis functions
- **test_database.py**: Unit tests for database operations

### Documentation (docs/)

- **API_SETUP.md**: Detailed guide for setting up API keys
- **DATABASE.md**: Database schema and operations documentation

### Assets (assets/)

- Placeholder for future static files (images, logos, etc.)

## Migration Steps

To migrate from the old structure to the new one:

1. **Update app.py**: Rewrite to use the new modular structure
2. **Remove old files**: Delete `app (1).py` and `news_api.py`
3. **Set up environment**: Copy `.env.example` to `.env` and add API keys
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Initialize database**: `python src/database/init_db.py`
6. **Run tests**: `python tests/test_sentiment.py` and `python tests/test_database.py`
7. **Run app**: `streamlit run app.py`

## Benefits of This Structure

- **Modularity**: Separation of concerns (API, utils, models, database)
- **Maintainability**: Easier to find and update code
- **Testability**: Isolated modules for unit testing
- **Scalability**: Easy to add new features or APIs
- **Security**: Environment variables for sensitive data
- **Documentation**: Clear documentation for setup and usage
- **Data Persistence**: SQLite database for storing articles and sentiment history
- **User Experience**: User preferences and search history for better UX
- **Performance**: Database indexes for fast queries
