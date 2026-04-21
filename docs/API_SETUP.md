# API Setup Guide

This guide explains how to set up API keys for various news sources.

## Supported APIs

### 1. Bing News Search API (Recommended)

**Free Tier:** 1,000 transactions per month

**Setup Steps:**
1. Go to [Azure Portal](https://portal.azure.com/)
2. Sign in with your Microsoft account
3. Click "Create a resource"
4. Search for "Bing News Search"
5. Click "Create"
6. Fill in the required fields:
   - Resource name: Choose a unique name
   - Pricing tier: Free (F0)
   - Region: Choose your nearest region
7. Click "Review + create" then "Create"
8. Once deployed, go to "Keys and Endpoint"
9. Copy one of the API keys
10. Add it to your `.env` file:
   ```
   BING_API_KEY=your_key_here
   ```

**Documentation:** [Bing News Search API Docs](https://docs.microsoft.com/en-us/rest/api/cognitiveservices-bingsearch/bing-news-api-v7-overview)

---

### 2. NewsAPI

**Free Tier:** Limited requests per day

**Setup Steps:**
1. Go to [NewsAPI](https://newsapi.org/)
2. Click "Get API Key"
3. Sign up with your email
4. Verify your email address
5. Copy your API key from the dashboard
6. Add it to your `.env` file:
   ```
   NEWSAPI_KEY=your_key_here
   ```

**Documentation:** [NewsAPI Docs](https://newsapi.org/docs)

---

### 3. GNews

**Free Tier:** 100 requests per day

**Setup Steps:**
1. Go to [GNews](https://gnews.io/)
2. Click "Get API Key"
3. Sign up with your email
4. Verify your email address
5. Copy your API key from the dashboard
6. Add it to your `.env` file:
   ```
   GNEWS_API_KEY=your_key_here
   ```

**Documentation:** [GNews Docs](https://gnews.io/docs)

---

## Environment Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Add your API keys to `.env`:
   ```
   BING_API_KEY=your_bing_key_here
   NEWSAPI_KEY=your_newsapi_key_here
   GNEWS_API_KEY=your_gnews_key_here
   ```

3. The app will automatically load the keys when it starts.

---

## Switching Between APIs

To switch between APIs, modify the `get_news_fetcher()` call in your app:

```python
# Use Bing (recommended)
fetcher = get_news_fetcher("bing")

# Use NewsAPI
fetcher = get_news_fetcher("newsapi")

# Use GNews
fetcher = get_news_fetcher("gnews")
```

---

## Troubleshooting

### API Key Not Working
- Verify the key is correct (no extra spaces)
- Check if the key is still valid
- Ensure you haven't exceeded the free tier limits

### DNS Resolution Errors
- Check your internet connection
- Try using a different API
- Contact the API provider if the issue persists

### Rate Limiting
- Free tiers have daily/monthly limits
- Consider upgrading to a paid plan for higher limits
- Implement caching to reduce API calls
