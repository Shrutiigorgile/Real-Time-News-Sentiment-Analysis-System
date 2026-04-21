"""
Helper functions for data processing and formatting
"""
import pandas as pd
from datetime import datetime


def articles_to_dataframe(articles):
    """
    Convert articles list to pandas DataFrame

    Args:
        articles: List of article dictionaries

    Returns:
        pandas DataFrame with article data
    """
    data = []
    for article in articles:
        if not article.get("title") or not article.get("url"):
            continue

        data.append({
            "Title": article.get("title", ""),
            "Source": article.get("source", {}).get("name", "Unknown"),
            "Date": article.get("publishedAt", "")[:10] if article.get("publishedAt") else "",
            "Sentiment": article.get("sentiment_label", "Neutral"),
            "URL": article.get("url", "")
        })

    return pd.DataFrame(data)


def extract_text(articles):
    """
    Extract all text from articles for word cloud generation

    Args:
        articles: List of article dictionaries

    Returns:
        String containing all text from articles
    """
    all_text = ""
    for article in articles:
        text = article.get("content") or article.get("description") or ""
        all_text += " " + text
    return all_text


def get_current_timestamp():
    """
    Get current timestamp in formatted string

    Returns:
        String with current date and time
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_date(date_string):
    """
    Format date string for display

    Args:
        date_string: Date string in ISO format

    Returns:
        Formatted date string (YYYY-MM-DD)
    """
    if not date_string:
        return ""
    return date_string[:10]
