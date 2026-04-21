"""
Unit tests for sentiment analysis
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.sentiment import get_sentiment, get_sentiment_label


def test_get_sentiment():
    """Test sentiment analysis"""
    positive_text = "This is a great and wonderful news!"
    negative_text = "This is terrible and awful news."
    neutral_text = "This is just regular news."

    assert get_sentiment(positive_text) > 0
    assert get_sentiment(negative_text) < 0
    assert get_sentiment(neutral_text) == 0
    assert get_sentiment("") == 0

    print("✓ Sentiment analysis tests passed")


def test_get_sentiment_label():
    """Test sentiment labeling"""
    assert get_sentiment_label(0.5) == "Positive"
    assert get_sentiment_label(-0.5) == "Negative"
    assert get_sentiment_label(0.0) == "Neutral"

    print("✓ Sentiment labeling tests passed")


if __name__ == "__main__":
    test_get_sentiment()
    test_get_sentiment_label()
    print("\nAll tests passed!")
