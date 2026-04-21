"""
Database models for the News Sentiment Dashboard
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json


class Database:
    """SQLite database manager for news articles and sentiment data"""

    def __init__(self, db_path: str = "news_dashboard.db"):
        """
        Initialize database connection

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()

        # Articles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                source TEXT,
                description TEXT,
                content TEXT,
                published_at TEXT,
                category TEXT,
                image_url TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Sentiment analysis table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentiment_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                sentiment_score REAL,
                sentiment_label TEXT,
                analyzed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE
            )
        """)

        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Search history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                from_date TEXT,
                to_date TEXT,
                article_count INTEGER,
                searched_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes for better performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_articles_category
            ON articles(category)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_articles_published_at
            ON articles(published_at)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sentiment_label
            ON sentiment_analysis(sentiment_label)
        """)

        self.conn.commit()

    def insert_article(self, article: Dict, category: str) -> Optional[int]:
        """
        Insert or update an article in the database

        Args:
            article: Article dictionary
            category: News category

        Returns:
            Article ID if successful, None otherwise
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO articles
                (title, url, source, description, content, published_at, category, image_url, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article.get("title", ""),
                article.get("url", ""),
                article.get("source", {}).get("name", "Unknown"),
                article.get("description", ""),
                article.get("content", ""),
                article.get("publishedAt", ""),
                category,
                article.get("urlToImage", ""),
                datetime.now().isoformat()
            ))

            self.conn.commit()
            return cursor.lastrowid

        except sqlite3.Error as e:
            print(f"Error inserting article: {e}")
            return None

    def insert_sentiment(self, article_id: int, sentiment_score: float, sentiment_label: str):
        """
        Insert sentiment analysis result

        Args:
            article_id: ID of the article
            sentiment_score: Sentiment polarity score
            sentiment_label: Sentiment label (Positive/Negative/Neutral)
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO sentiment_analysis
                (article_id, sentiment_score, sentiment_label)
                VALUES (?, ?, ?)
            """, (article_id, sentiment_score, sentiment_label))

            self.conn.commit()

        except sqlite3.Error as e:
            print(f"Error inserting sentiment: {e}")

    def get_articles_by_category(self, category: str, limit: int = 20) -> List[Dict]:
        """
        Get articles by category with sentiment analysis

        Args:
            category: News category
            limit: Maximum number of articles to return

        Returns:
            List of article dictionaries with sentiment
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                a.*,
                s.sentiment_score,
                s.sentiment_label
            FROM articles a
            LEFT JOIN sentiment_analysis s ON a.id = s.article_id
            WHERE a.category = ?
            ORDER BY a.published_at DESC
            LIMIT ?
        """, (category, limit))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_articles_by_date_range(self, from_date: str, to_date: str, category: str = None, limit: int = 20) -> List[Dict]:
        """
        Get articles by date range

        Args:
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            category: Optional category filter
            limit: Maximum number of articles

        Returns:
            List of article dictionaries
        """
        cursor = self.conn.cursor()

        if category:
            cursor.execute("""
                SELECT
                    a.*,
                    s.sentiment_score,
                    s.sentiment_label
                FROM articles a
                LEFT JOIN sentiment_analysis s ON a.id = s.article_id
                WHERE a.category = ?
                AND DATE(a.published_at) BETWEEN ? AND ?
                ORDER BY a.published_at DESC
                LIMIT ?
            """, (category, from_date, to_date, limit))
        else:
            cursor.execute("""
                SELECT
                    a.*,
                    s.sentiment_score,
                    s.sentiment_label
                FROM articles a
                LEFT JOIN sentiment_analysis s ON a.id = s.article_id
                WHERE DATE(a.published_at) BETWEEN ? AND ?
                ORDER BY a.published_at DESC
                LIMIT ?
            """, (from_date, to_date, limit))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_sentiment_summary(self, category: str = None) -> Dict:
        """
        Get sentiment analysis summary

        Args:
            category: Optional category filter

        Returns:
            Dictionary with sentiment counts
        """
        cursor = self.conn.cursor()

        if category:
            cursor.execute("""
                SELECT
                    s.sentiment_label,
                    COUNT(*) as count
                FROM sentiment_analysis s
                JOIN articles a ON s.article_id = a.id
                WHERE a.category = ?
                GROUP BY s.sentiment_label
            """, (category,))
        else:
            cursor.execute("""
                SELECT
                    sentiment_label,
                    COUNT(*) as count
                FROM sentiment_analysis
                GROUP BY sentiment_label
            """)

        rows = cursor.fetchall()
        summary = {row["sentiment_label"]: row["count"] for row in rows}

        # Ensure all labels are present
        for label in ["Positive", "Negative", "Neutral"]:
            if label not in summary:
                summary[label] = 0

        return summary

    def save_preference(self, key: str, value: str):
        """
        Save user preference

        Args:
            key: Preference key
            value: Preference value
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
            VALUES (?, ?, ?)
        """, (key, value, datetime.now().isoformat()))

        self.conn.commit()

    def get_preference(self, key: str, default: str = None) -> Optional[str]:
        """
        Get user preference

        Args:
            key: Preference key
            default: Default value if not found

        Returns:
            Preference value or default
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT value FROM user_preferences WHERE key = ?
        """, (key,))

        row = cursor.fetchone()
        return row["value"] if row else default

    def log_search(self, category: str, from_date: str, to_date: str, article_count: int):
        """
        Log search history

        Args:
            category: Category searched
            from_date: Start date
            to_date: End date
            article_count: Number of articles found
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO search_history (category, from_date, to_date, article_count)
            VALUES (?, ?, ?, ?)
        """, (category, from_date, to_date, article_count))

        self.conn.commit()

    def get_search_history(self, limit: int = 10) -> List[Dict]:
        """
        Get recent search history

        Args:
            limit: Maximum number of records

        Returns:
            List of search history records
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM search_history
            ORDER BY searched_at DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def delete_old_articles(self, days: int = 30):
        """
        Delete articles older than specified days

        Args:
            days: Number of days to keep
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            DELETE FROM articles
            WHERE DATE(published_at) < DATE('now', '-' || ? || ' days')
        """, (days,))

        deleted_count = cursor.rowcount
        self.conn.commit()

        return deleted_count

    def get_statistics(self) -> Dict:
        """
        Get database statistics

        Returns:
            Dictionary with database statistics
        """
        cursor = self.conn.cursor()

        stats = {}

        # Total articles
        cursor.execute("SELECT COUNT(*) as count FROM articles")
        stats["total_articles"] = cursor.fetchone()["count"]

        # Articles by category
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM articles
            GROUP BY category
        """)
        stats["articles_by_category"] = {row["category"]: row["count"] for row in cursor.fetchall()}

        # Total sentiment analyses
        cursor.execute("SELECT COUNT(*) as count FROM sentiment_analysis")
        stats["total_sentiment_analyses"] = cursor.fetchone()["count"]

        # Database size
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        stats["database_size_bytes"] = cursor.fetchone()["size"]

        return stats

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Destructor to close connection"""
        self.close()
