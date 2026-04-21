"""
Unit tests for database operations
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tempfile
import os
from src.database.models import Database


def test_database_initialization():
    """Test database initialization"""
    # Create temporary database
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name

    try:
        db = Database(db_path)
        assert db.conn is not None
        db.close()
        print("✓ Database initialization test passed")
    finally:
        os.unlink(db_path)


def test_insert_article():
    """Test article insertion"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name

    try:
        db = Database(db_path)

        article = {
            "title": "Test Article",
            "url": "https://example.com/test",
            "source": {"name": "Test Source"},
            "description": "Test description",
            "content": "Test content",
            "publishedAt": "2024-01-01T00:00:00Z"
        }

        article_id = db.insert_article(article, "Business")
        assert article_id is not None
        assert article_id > 0

        db.close()
        print("✓ Article insertion test passed")
    finally:
        os.unlink(db_path)


def test_insert_sentiment():
    """Test sentiment insertion"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name

    try:
        db = Database(db_path)

        # Insert article first
        article = {
            "title": "Test Article",
            "url": "https://example.com/test2",
            "source": {"name": "Test Source"},
            "publishedAt": "2024-01-01T00:00:00Z"
        }
        article_id = db.insert_article(article, "Technology")

        # Insert sentiment
        db.insert_sentiment(article_id, 0.5, "Positive")

        # Verify
        summary = db.get_sentiment_summary()
        assert summary["Positive"] == 1

        db.close()
        print("✓ Sentiment insertion test passed")
    finally:
        os.unlink(db_path)


def test_get_articles_by_category():
    """Test fetching articles by category"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name

    try:
        db = Database(db_path)

        # Insert test articles
        for i in range(3):
            article = {
                "title": f"Test Article {i}",
                "url": f"https://example.com/test{i}",
                "source": {"name": "Test Source"},
                "publishedAt": "2024-01-01T00:00:00Z"
            }
            db.insert_article(article, "Business")

        # Fetch articles
        articles = db.get_articles_by_category("Business")
        assert len(articles) == 3

        db.close()
        print("✓ Get articles by category test passed")
    finally:
        os.unlink(db_path)


def test_user_preferences():
    """Test user preferences"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name

    try:
        db = Database(db_path)

        # Save preference
        db.save_preference("test_key", "test_value")

        # Get preference
        value = db.get_preference("test_key")
        assert value == "test_value"

        # Get non-existent preference
        value = db.get_preference("non_existent", "default")
        assert value == "default"

        db.close()
        print("✓ User preferences test passed")
    finally:
        os.unlink(db_path)


if __name__ == "__main__":
    test_database_initialization()
    test_insert_article()
    test_insert_sentiment()
    test_get_articles_by_category()
    test_user_preferences()
    print("\nAll database tests passed!")
