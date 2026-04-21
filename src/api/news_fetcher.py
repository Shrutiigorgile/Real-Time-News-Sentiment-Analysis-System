"""
News fetcher module for fetching news from various APIs
"""
import requests
from datetime import datetime, timedelta
from config import Config


class NewsFetcher:
    """Base class for news fetching"""

    def __init__(self):
        self.timeout = Config.TIMEOUT
        self.page_size = Config.PAGE_SIZE

    def fetch(self, category, from_date=None, to_date=None):
        """Fetch news articles - to be implemented by subclasses"""
        raise NotImplementedError


class BingNewsFetcher(NewsFetcher):
    """Fetch news from Bing News Search API"""

    def fetch(self, category, from_date=None, to_date=None):
        """
        Fetch news articles from Bing News Search API

        Args:
            category: News category
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            List of article dictionaries
        """
        query = Config.CATEGORIES.get(category, "news")

        params = {
            "q": query,
            "mkt": "en-US",
            "count": self.page_size,
            "safeSearch": "Moderate",
            "textFormat": "HTML",
            "sortBy": "Date"
        }

        headers = {
            "Ocp-Apim-Subscription-Key": Config.BING_API_KEY
        }

        try:
            response = requests.get(
                Config.BING_API_URL,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            data = response.json()

            if "value" not in data:
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return []

            # Transform Bing response to standard format
            articles = []
            for item in data.get("value", []):
                articles.append({
                    "title": item.get("name", ""),
                    "description": item.get("description", ""),
                    "content": item.get("description", ""),
                    "url": item.get("url", ""),
                    "publishedAt": item.get("datePublished", ""),
                    "source": {
                        "name": item.get("provider", [{}])[0].get("name", "Unknown")
                        if item.get("provider") else "Unknown"
                    }
                })

            return articles

        except Exception as e:
            print(f"Error fetching news from Bing: {e}")
            return []


class NewsAPIFetcher(NewsFetcher):
    """Fetch news from NewsAPI"""

    def fetch(self, category, from_date=None, to_date=None):
        """
        Fetch news articles from NewsAPI

        Args:
            category: News category
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            List of article dictionaries
        """
        query = Config.CATEGORIES.get(category, "news")

        # Get date range: last 7 days if not specified
        if from_date and to_date:
            date_from = from_date
            date_to = to_date
        else:
            date_to = datetime.now().strftime("%Y-%m-%d")
            date_from = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        params = {
            "q": query,
            "language": Config.LANGUAGE,
            "sortBy": "publishedAt",
            "pageSize": self.page_size,
            "from": date_from,
            "to": date_to,
            "apiKey": Config.NEWSAPI_KEY
        }

        try:
            response = requests.get(
                Config.NEWSAPI_URL,
                params=params,
                timeout=self.timeout
            )
            data = response.json()

            if data.get("status") == "error":
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return []

            return data.get("articles", [])

        except Exception as e:
            print(f"Error fetching news from NewsAPI: {e}")
            return []


class GNewsFetcher(NewsFetcher):
    """Fetch news from GNews API"""

    def fetch(self, category, from_date=None, to_date=None):
        """
        Fetch news articles from GNews API

        Args:
            category: News category
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            List of article dictionaries
        """
        query = Config.CATEGORIES.get(category, "general")

        params = {
            "category": query,
            "lang": "en",
            "max": self.page_size,
            "apikey": Config.GNEWS_API_KEY
        }

        try:
            response = requests.get(
                Config.GNEWS_API_URL,
                params=params,
                timeout=self.timeout
            )
            data = response.json()

            if "articles" not in data:
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return []

            return data.get("articles", [])

        except Exception as e:
            print(f"Error fetching news from GNews: {e}")
            return []


def get_news_fetcher(api_source="bing"):
    """
    Factory function to get the appropriate news fetcher

    Args:
        api_source: API source ("bing", "newsapi", "gnews")

    Returns:
        NewsFetcher instance
    """
    fetchers = {
        "bing": BingNewsFetcher,
        "newsapi": NewsAPIFetcher,
        "gnews": GNewsFetcher
    }

    fetcher_class = fetchers.get(api_source.lower(), BingNewsFetcher)
    return fetcher_class()
