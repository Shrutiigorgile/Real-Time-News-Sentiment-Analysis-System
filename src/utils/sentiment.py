"""
Sentiment analysis utilities using TextBlob
"""
from textblob import TextBlob
from config import Config


def get_sentiment(text):
    """
    Get sentiment polarity score for given text

    Args:
        text: Text to analyze

    Returns:
        Sentiment polarity score between -1 (negative) and 1 (positive)
    """
    if not text:
        return 0
    return TextBlob(text).sentiment.polarity


def get_sentiment_label(score):
    """
    Get sentiment label based on polarity score

    Args:
        score: Sentiment polarity score

    Returns:
        "Positive", "Negative", or "Neutral"
    """
    if score > Config.POSITIVE_THRESHOLD:
        return "Positive"
    elif score < Config.NEGATIVE_THRESHOLD:
        return "Negative"
    else:
        return "Neutral"


def analyze_article(article):
    """
    Analyze sentiment of a news article

    Args:
        article: Article dictionary with title, description, or content

    Returns:
        Article dictionary with added sentiment information
    """
    text = article.get("content") or article.get("description") or article.get("title", "")
    score = get_sentiment(text)
    label = get_sentiment_label(score)

    article["sentiment_score"] = score
    article["sentiment_label"] = label

    return article
