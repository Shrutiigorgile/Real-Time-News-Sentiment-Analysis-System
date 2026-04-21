"""
Database initialization script
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.models import Database


def init_database(db_path: str = "news_dashboard.db"):
    """
    Initialize the database with tables

    Args:
        db_path: Path to database file
    """
    print(f"Initializing database at: {db_path}")
    
    db = Database(db_path)
    
    print("✓ Database initialized successfully")
    print("✓ Tables created:")
    print("  - articles")
    print("  - sentiment_analysis")
    print("  - user_preferences")
    print("  - search_history")
    
    # Get initial statistics
    stats = db.get_statistics()
    print(f"\nDatabase statistics:")
    print(f"  - Total articles: {stats['total_articles']}")
    print(f"  - Database size: {stats['database_size_bytes']} bytes")
    
    db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize News Dashboard Database")
    parser.add_argument(
        "--db-path",
        default="news_dashboard.db",
        help="Path to database file (default: news_dashboard.db)"
    )
    
    args = parser.parse_args()
    init_database(args.db_path)
