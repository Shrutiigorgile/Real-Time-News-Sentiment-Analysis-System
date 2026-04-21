"""
Category definitions and mappings
"""
from config import Config


def get_categories():
    """
    Get available news categories

    Returns:
        List of category names
    """
    return list(Config.CATEGORIES.keys())


def get_category_query(category):
    """
    Get API query string for a category

    Args:
        category: Category name

    Returns:
        Query string for the category
    """
    return Config.CATEGORIES.get(category, "news")


def is_valid_category(category):
    """
    Check if a category is valid

    Args:
        category: Category name to check

    Returns:
        True if category is valid, False otherwise
    """
    return category in Config.CATEGORIES
