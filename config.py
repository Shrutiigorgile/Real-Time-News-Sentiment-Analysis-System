import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the News Sentiment Dashboard"""

    # API Configuration
    BING_API_KEY = os.getenv("BING_API_KEY", "")
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
    GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "")

    # API Endpoints
    BING_API_URL = "https://api.bing.microsoft.com/v7.0/news/search"
    NEWSAPI_URL = "https://newsapi.org/v2/everything"
    NEWSAPI_TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
    GNEWS_API_URL = "https://gnews.io/api/v4/top-headlines"

    # Category Mappings
    CATEGORIES = {
        "Business": "business",
        "Technology": "technology",
        "Sports": "sports",
        "Health": "health",
        "Politics": "politics",
        "Entertainment": "entertainment"
    }

    # Default Settings
    LANGUAGE = "en"
    PAGE_SIZE = 20
    TIMEOUT = 10

    # App Settings
    APP_TITLE = "News Sentiment Analysis Dashboard"
    APP_LAYOUT = "wide"

    # Sentiment Thresholds
    POSITIVE_THRESHOLD = 0.1
    NEGATIVE_THRESHOLD = -0.1
