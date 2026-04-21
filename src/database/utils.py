"""
Database utility functions for the News Sentiment Dashboard
"""
from typing import List, Dict
from src.database.models import Database


class ArticleManager:
    """Manager for article database operations"""

    def __init__(self, db: Database):
        """
        Initialize article manager

        Args:
            db: Database instance
        """
        self.db = db

    def save_articles_with_sentiment(self, articles: List[Dict], category: str) -> int:
        """
        Save articles with sentiment analysis to database

        Args:
            articles: List of article dictionaries
            category: News category

        Returns:
            Number of articles saved
        """
        from src.utils.sentiment import get_sentiment, get_sentiment_label

        saved_count = 0

        for article in articles:
            # Insert article
            article_id = self.db.insert_article(article, category)

            if article_id:
                # Analyze sentiment
                text = article.get("content") or article.get("description") or ""
                score = get_sentiment(text)
                label = get_sentiment_label(score)

                # Save sentiment
                self.db.insert_sentiment(article_id, score, label)
                saved_count += 1

        return saved_count

    def get_articles_for_dashboard(self, category: str, from_date: str = None, to_date: str = None, limit: int = 20) -> List[Dict]:
        """
        Get articles formatted for dashboard display

        Args:
            category: News category
            from_date: Optional start date
            to_date: Optional end date
            limit: Maximum articles to return

        Returns:
            List of formatted article dictionaries
        """
        if from_date and to_date:
            articles = self.db.get_articles_by_date_range(from_date, to_date, category, limit)
        else:
            articles = self.db.get_articles_by_category(category, limit)

        # Format for dashboard
        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                "Title": article.get("title", ""),
                "Source": article.get("source", "Unknown"),
                "Date": article.get("published_at", "")[:10] if article.get("published_at") else "",
                "Sentiment": article.get("sentiment_label", "Neutral"),
                "URL": article.get("url", ""),
                "Description": article.get("description", "")
            })

        return formatted_articles

    def get_sentiment_metrics(self, category: str = None) -> Dict[str, int]:
        """
        Get sentiment metrics for dashboard

        Args:
            category: Optional category filter

        Returns:
            Dictionary with sentiment counts
        """
        return self.db.get_sentiment_summary(category)


class PreferenceManager:
    """Manager for user preferences"""

    def __init__(self, db: Database):
        """
        Initialize preference manager

        Args:
            db: Database instance
        """
        self.db = db

    def save_category(self, category: str):
        """Save last selected category"""
        self.db.save_preference("last_category", category)

    def get_last_category(self) -> str:
        """Get last selected category"""
        return self.db.get_preference("last_category", "Business")

    def save_date_range(self, from_date: str, to_date: str):
        """Save last used date range"""
        self.db.save_preference("last_from_date", from_date)
        self.db.save_preference("last_to_date", to_date)

    def get_last_date_range(self) -> tuple:
        """Get last used date range"""
        from_date = self.db.get_preference("last_from_date")
        to_date = self.db.get_preference("last_to_date")
        return (from_date, to_date)

    def save_api_source(self, api_source: str):
        """Save preferred API source"""
        self.db.save_preference("api_source", api_source)

    def get_api_source(self) -> str:
        """Get preferred API source"""
        return self.db.get_preference("api_source", "bing")


class SearchHistoryManager:
    """Manager for search history"""

    def __init__(self, db: Database):
        """
        Initialize search history manager

        Args:
            db: Database instance
        """
        self.db = db

    def log_search(self, category: str, from_date: str, to_date: str, article_count: int):
        """Log a search query"""
        self.db.log_search(category, from_date, to_date, article_count)

    def get_recent_searches(self, limit: int = 10) -> List[Dict]:
        """Get recent search history"""
        return self.db.get_search_history(limit)
