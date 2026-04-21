# Database Documentation

## Overview

The News Sentiment Dashboard uses SQLite to store articles, sentiment analysis results, user preferences, and search history. The database is automatically initialized when you run the initialization script.

## Database Schema

### 1. Articles Table

Stores news articles fetched from APIs.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| title | TEXT | Article title |
| url | TEXT | Article URL (unique) |
| source | TEXT | Source name |
| description | TEXT | Article description |
| content | TEXT | Full article content |
| published_at | TEXT | Publication date (ISO format) |
| category | TEXT | News category |
| image_url | TEXT | Article image URL |
| created_at | TEXT | Record creation timestamp |
| updated_at | TEXT | Record update timestamp |

**Indexes:**
- `idx_articles_category` on category column
- `idx_articles_published_at` on published_at column

### 2. Sentiment Analysis Table

Stores sentiment analysis results for articles.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| article_id | INTEGER | Foreign key to articles table |
| sentiment_score | REAL | Sentiment polarity score (-1 to 1) |
| sentiment_label | TEXT | Sentiment label (Positive/Negative/Neutral) |
| analyzed_at | TEXT | Analysis timestamp |

**Foreign Key:** `article_id` references `articles(id)` with CASCADE delete

**Indexes:**
- `idx_sentiment_label` on sentiment_label column

### 3. User Preferences Table

Stores user preferences and settings.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| key | TEXT | Preference key (unique) |
| value | TEXT | Preference value |
| updated_at | TEXT | Last update timestamp |

**Common Keys:**
- `last_category`: Last selected category
- `last_from_date`: Last used start date
- `last_to_date`: Last used end date
- `api_source`: Preferred API source

### 4. Search History Table

Stores search history for analytics and quick access.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| category | TEXT | Category searched |
| from_date | TEXT | Search start date |
| to_date | TEXT | Search end date |
| article_count | INTEGER | Number of articles found |
| searched_at | TEXT | Search timestamp |

## Initialization

To initialize the database:

```bash
python src/database/init_db.py
```

This will create the database file (`news_dashboard.db`) and all tables with indexes.

## Database Operations

### Using the Database Class

```python
from src.database.models import Database

# Initialize database
db = Database("news_dashboard.db")

# Insert article
article_id = db.insert_article(article_dict, "Business")

# Insert sentiment
db.insert_sentiment(article_id, 0.5, "Positive")

# Get articles by category
articles = db.get_articles_by_category("Business", limit=20)

# Get sentiment summary
summary = db.get_sentiment_summary("Business")

# Close connection
db.close()
```

### Using Utility Managers

```python
from src.database.models import Database
from src.database.utils import ArticleManager, PreferenceManager

# Initialize
db = Database("news_dashboard.db")
article_manager = ArticleManager(db)
pref_manager = PreferenceManager(db)

# Save articles with sentiment
saved = article_manager.save_articles_with_sentiment(articles, "Business")

# Get articles for dashboard
articles = article_manager.get_articles_for_dashboard("Business")

# Save/restore preferences
pref_manager.save_category("Technology")
last_category = pref_manager.get_last_category()

# Close
db.close()
```

## Database Maintenance

### Deleting Old Articles

To delete articles older than a specified number of days:

```python
from src.database.models import Database

db = Database("news_dashboard.db")
deleted = db.delete_old_articles(days=30)
print(f"Deleted {deleted} old articles")
db.close()
```

### Getting Statistics

```python
from src.database.models import Database

db = Database("news_dashboard.db")
stats = db.get_statistics()
print(f"Total articles: {stats['total_articles']}")
print(f"Database size: {stats['database_size_bytes']} bytes")
db.close()
```

## Database Location

By default, the database file is created in the project root as `news_dashboard.db`. You can specify a custom path:

```python
db = Database("/path/to/custom/database.db")
```

## Backup and Restore

### Backup

```bash
# Copy the database file
cp news_dashboard.db news_dashboard_backup.db
```

### Restore

```bash
# Restore from backup
cp news_dashboard_backup.db news_dashboard.db
```

## Performance Considerations

- **Indexes**: The database includes indexes on frequently queried columns (category, published_at, sentiment_label)
- **Connection Pooling**: For production use, consider implementing connection pooling
- **Batch Operations**: Use batch inserts for better performance when saving multiple articles
- **Cleanup**: Regularly clean up old articles to prevent database bloat

## Troubleshooting

### Database Locked Error

If you encounter "database is locked" errors:
- Ensure only one process is accessing the database
- Close all database connections before opening new ones
- Use `db.close()` explicitly when done

### Corrupted Database

If the database becomes corrupted:
```bash
# Recover using SQLite command line
sqlite3 news_dashboard.db ".recover" | sqlite3 recovered.db
```

### Missing Tables

If tables are missing, reinitialize the database:
```bash
python src/database/init_db.py
```

## Migration

To modify the database schema:
1. Create a migration script in `src/database/migrations/`
2. Update the `create_tables()` method in `models.py`
3. Document the migration in this file

Example migration script:
```python
def migrate_add_new_column():
    db = Database("news_dashboard.db")
    cursor = db.conn.cursor()
    cursor.execute("ALTER TABLE articles ADD COLUMN new_column TEXT")
    db.conn.commit()
    db.close()
```
