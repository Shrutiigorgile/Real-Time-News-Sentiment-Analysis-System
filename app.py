"""
News Sentiment Analysis Dashboard - Main Application
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Import from modular structure
from config import Config
from src.api.news_fetcher import get_news_fetcher
from src.utils.sentiment import get_sentiment, get_sentiment_label
from src.utils.helpers import extract_text
from src.database.models import Database
from src.database.utils import ArticleManager, PreferenceManager, SearchHistoryManager

# ---------------- PAGE SETUP ---------------- #
st.set_page_config(
    page_title=Config.APP_TITLE,
    layout=Config.APP_LAYOUT,
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
    .main {
        background-color: #1a1a1a;
        color: #e0e0e0;
    }
    .stApp {
        background-color: #1a1a1a;
    }
    h1 {
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
    }
    h2 {
        color: #e0e0e0;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    h3 {
        color: #ffffff;
    }
    p {
        color: #b0b0b0;
    }
    .metric-card {
        background: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        margin: 10px 0;
    }
    .article-card {
        background: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        margin: 15px 0;
        border-left: 4px solid #60a5fa;
    }
    .positive {
        border-left-color: #4ade80;
    }
    .negative {
        border-left-color: #f87171;
    }
    .neutral {
        border-left-color: #fbbf24;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
    }
    div[data-testid="stMetricLabel"] {
        color: #a0a0a0;
    }
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
    .stSelectbox>div>div {
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    .stDateInput>div>div {
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    div[data-testid="stExpander"] {
        background-color: #2d2d2d;
    }
    .stProgress > div > div > div {
        background-color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE INITIALIZATION ---------------- #
@st.cache_resource
def get_database():
    """Initialize database connection (cached)"""
    return Database("news_dashboard.db")

db = get_database()
article_manager = ArticleManager(db)
pref_manager = PreferenceManager(db)
history_manager = SearchHistoryManager(db)

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.markdown("# 🧠 Dashboard")
    st.markdown("---")

    st.markdown("### ⚙️ Settings")

    # API Source Selection
    api_source = st.selectbox(
        "🔌 API Source",
        ["GNews", "NewsAPI", "Bing"],
        index=0
    )

    api_source_map = {
        "GNews": "gnews",
        "NewsAPI": "newsapi",
        "Bing": "bing"
    }
    selected_api = api_source_map[api_source]

    st.markdown("---")
    st.markdown("### 📊 Quick Stats")

    # Database stats in sidebar
    sidebar_stats = db.get_statistics()

    st.metric("Total Articles", sidebar_stats['total_articles'])
    st.metric("DB Size", f"{sidebar_stats['database_size_bytes']//1024} KB")

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption("Built with Streamlit, SQLite, and TextBlob")

# ---------------- MAIN CONTENT ---------------- #
st.markdown("# News Sentiment Analysis Dashboard")
st.caption("Analyze news sentiment across categories with real-time insights")

# ---------------- REFRESH BUTTON ---------------- #
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

# ---------------- CONTROLS SECTION ---------------- #
st.markdown("## 📋 Filters & Controls")

col1, col2, col3 = st.columns(3)

with col1:
    categories = Config.CATEGORIES.keys()
    selected_category = st.selectbox(
        "📂 Category",
        list(categories),
        index=list(categories).index(pref_manager.get_last_category())
    )

with col2:
    from_date = st.date_input("📅 From", value=datetime.now() - timedelta(days=7))

with col3:
    to_date = st.date_input("📅 To", value=datetime.now())

# ---------------- MAIN LOGIC ---------------- #
if selected_category:

    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.text("🔄 Fetching news from API...")
    progress_bar.progress(25)

    with st.spinner("Fetching and analyzing news..."):

        # Convert date objects to strings
        from_date_str = from_date.strftime("%Y-%m-%d")
        to_date_str = to_date.strftime("%Y-%m-%d")

        # Fetch news from API
        fetcher = get_news_fetcher(selected_api)
        articles = fetcher.fetch(selected_category, from_date_str, to_date_str)

        progress_bar.progress(50)
        status_text.text("💾 Saving to database...")

        if not articles:
            st.warning("⚠️ No articles found. Please try a different category or check your API key.")
            progress_bar.empty()
            status_text.empty()
            st.stop()

        # Save articles to database with sentiment
        saved_count = article_manager.save_articles_with_sentiment(articles, selected_category)

        progress_bar.progress(75)
        status_text.text("📊 Processing data...")

        # Get articles from database for display
        data = article_manager.get_articles_for_dashboard(selected_category, from_date_str, to_date_str)
        
        if not data:
            st.warning("⚠️ No articles found in database for the selected criteria.")
            progress_bar.empty()
            status_text.empty()
            st.stop()

        df = pd.DataFrame(data)

        # Log search history
        history_manager.log_search(selected_category, from_date_str, to_date_str, len(data))

        # Save user preferences
        pref_manager.save_category(selected_category)
        pref_manager.save_date_range(from_date_str, to_date_str)
        pref_manager.save_api_source(selected_api)

        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()

        st.success(f"✅ Successfully fetched and analyzed {saved_count} articles")

    # ---------------- TIME DISPLAY ---------------- #
    st.markdown(f"**🕒 Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ---------------- SENTIMENT SUMMARY ---------------- #
    st.markdown("## 📊 Sentiment Analysis")

    metrics = article_manager.get_sentiment_metrics(selected_category)
    pos = metrics.get("Positive", 0)
    neg = metrics.get("Negative", 0)
    neu = metrics.get("Neutral", 0)
    total = pos + neg + neu

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("😊 Positive", pos, delta=f"{(pos/total*100):.1f}%" if total > 0 else None)
    with col2:
        st.metric("😡 Negative", neg, delta=f"{(neg/total*100):.1f}%" if total > 0 else None)
    with col3:
        st.metric("😐 Neutral", neu, delta=f"{(neu/total*100):.1f}%" if total > 0 else None)
    with col4:
        st.metric("📰 Total", total)

    # ---------------- WORDCLOUD ---------------- #
    st.markdown("## ☁️ Word Cloud")

    # Extract text from articles
    all_text = extract_text(articles)

    if all_text.strip():
        try:
            wc = WordCloud(
                width=800,
                height=400,
                background_color="#2d2d2d",
                colormap="plasma",
                max_words=100,
                contour_color="#1a1a1a",
                contour_width=2
            ).generate(all_text)

            fig, ax = plt.subplots(figsize=(10, 5), facecolor='#1a1a1a')
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(fig)
            plt.close()
        except Exception as e:
            st.warning(f"⚠️ Could not generate word cloud: {e}")
    else:
        st.info("ℹ️ No text available for word cloud generation")

    # ---------------- FILTER NEWS ---------------- #
    st.markdown("## 🔍 Filter Articles")

    col1, col2 = st.columns([1, 2])
    with col1:
        filter_option = st.selectbox(
            "Filter by Sentiment",
            ["All", "Positive", "Negative", "Neutral"]
        )

    if filter_option != "All":
        df = df[df["Sentiment"] == filter_option]

    # ---------------- NEWS LIST ---------------- #
    st.markdown(f"## 📰 {selected_category} News ({len(df)} articles)")

    if df.empty:
        st.info("ℹ️ No articles match the selected filter.")
    else:
        for idx, (_, row) in enumerate(df.iterrows(), 1):
            sentiment_class = row['Sentiment'].lower()
            
            st.markdown(f"""
            <div class="article-card {sentiment_class}">
                <h3 style="margin-top: 0; color: #ffffff;">{idx}. {row['Title']}</h3>
                <p style="margin: 5px 0; color: #b0b0b0;">
                    <strong>Sentiment:</strong> <span style="color: {'#4ade80' if row['Sentiment'] == 'Positive' else '#f87171' if row['Sentiment'] == 'Negative' else '#fbbf24'}">{row['Sentiment']}</span>
                </p>
                <p style="margin: 5px 0; color: #909090; font-size: 0.9em;">
                    📰 {row['Source']} | 📅 {row['Date']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if row.get('Description'):
                st.caption(f"📝 {row['Description'][:250]}{'...' if len(row['Description']) > 250 else ''}")
            
            st.markdown(f"[🔗 Read Full Article]({row['URL']})")
            st.markdown("---")

    # ---------------- DATABASE STATISTICS ---------------- #
    with st.expander("📊 Detailed Database Statistics"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Overview")
            st.write(f"**Total Articles:** {sidebar_stats['total_articles']}")
            st.write(f"**Database Size:** {sidebar_stats['database_size_bytes']} bytes")
            st.write(f"**Sentiment Analyses:** {sidebar_stats['total_sentiment_analyses']}")

        with col2:
            st.markdown("### Articles by Category")
            for cat, count in sidebar_stats['articles_by_category'].items():
                st.write(f"📂 **{cat}:** {count} articles")

# ---------------- FOOTER ---------------- #
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a0a0a0; padding: 20px;">
    <p>🧠 <strong style="color: #ffffff;">News Sentiment Analysis Dashboard</strong></p>
    <p>Built with ❤️ using Streamlit, SQLite, and TextBlob</p>
</div>
""", unsafe_allow_html=True)
