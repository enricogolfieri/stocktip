import streamlit as st
from modules.news_fetcher import NewsFetcher
from modules.deepseek import DeepSeek, DeepSeekModels
from modules.analyzer import StockAnalyzer
from dotenv import load_dotenv
import modules.key as keys
import modules.logger as logger
import modules.finnhub as finnhub
import datetime

logger.init("GUI")

# API key status check
engine = DeepSeek(
    deepseek_api_key=keys.DeepSeekKey(),
    deepseek_model=DeepSeekModels.DEEPSEEK_CHAT,
)

analyzer = StockAnalyzer(ai_engine=engine)
fetcher = NewsFetcher(news_api_key=keys.NewsAPIKey())
finnhub_client = finnhub.Finnhub(
    key=keys.FinnhubAPIKey(),
)


def main():
    st.set_page_config(
        page_title="Stock Sentiment Analyzer", page_icon="📈", layout="wide"
    )

    st.title("📈 Stock Sentiment Analyzer")
    st.subheader("AI-Powered Trading Signals Using DeepSeek")

    # Sidebar for configuration
    st.sidebar.header("Configuration")

    for key in keys.iterate_keys():
        if key.exists():
            st.sidebar.success(f"✅ {key.description} key loaded")
            st.sidebar.text(key.value_to_string())
        else:
            st.sidebar.error(f"❌ {key.description} key missing")

    # Test DeepSeek API
    if st.sidebar.button("🔍 Test DeepSeek API"):
        with st.spinner("Testing DeepSeek API..."):
            success, message = engine.test_deepseek_api()
            if success:
                st.sidebar.success("✅ DeepSeek API is working!")
                st.sidebar.text(message)
            else:
                st.sidebar.error(f"❌ {message}")

    # Main interface
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Input")
        symbol = st.text_input(
            "Stock Symbol",
            placeholder="e.g., AAPL, TSLA, GOOGL",
            help="Enter the stock ticker symbol",
        ).upper()

        days = st.slider("News Analysis Period (days)", 1, 30, 7)

        analyze_button = st.button("🔍 Analyze Stock", type="primary")

    with col2:
        st.header("Analysis Results")

        if analyze_button and symbol:
            articles = []
            with st.spinner(f"Analyzing {symbol}..."):
                st.info("📰 Fetching news articles from NewsAPI...")
                success, newsapi_articles = fetcher.fetch_news_api(symbol, days, 10)
                if not success:
                    st.error(f"Error fetching NewsAPI news: {newsapi_articles}")
                else:
                    articles.extend(newsapi_articles)

                st.info("📊 Fetching news articles from FinViz")
                success, finviz_articles = fetcher.fetch_finviz_news(symbol, 10)
                if not success:
                    st.error(f"Error fetching FinViz news: {finviz_articles}")
                else:
                    articles.extend(finviz_articles)

                st.info("📈 Fetching insider sentiment data from Finnhub...")
                from_date = (
                    datetime.datetime.now() - datetime.timedelta(days=days)
                ).strftime("%Y-%m-%d")
                to_date = datetime.datetime.now().strftime("%Y-%m-%d")
                success, insider_sentiments = (
                    finnhub_client.get_stock_insider_sentiment(
                        symbol,
                        from_date,
                        to_date,
                    )
                )

                if not success:
                    st.error(f"Error fetching insider sentiment: {insider_sentiments}")
                else:
                    st.success("✅ Insider sentiment data fetched successfully")
                    logger.info(
                        f"Number of Insider Transactions for {symbol}: {len(insider_sentiments)}"
                    )

                st.info("📊 Fetching analyst sentiment data from Finnhub...")
                success, analyst_sentiments = (
                    finnhub_client.get_stock_recommendations_trends(symbol)
                )
                if not success:
                    st.error(f"Error fetching analyst sentiment: {analyst_sentiments}")
                else:
                    st.success("✅ Analyst sentiment data fetched successfully")
                    logger.info(
                        f"Number of Analyst Recommendations for {symbol}: {len(analyst_sentiments)}"
                    )

                st.info("🤖 Getting AI analysis from DeepSeek...")
                analysis = analyzer.analyze(
                    symbol, articles, insider_sentiments, analyst_sentiments
                )

            # Display results
            if isinstance(analysis, dict):
                signal = analysis.get("signal", "UNKNOWN")
                confidence = analysis.get("confidence", 0)

                # Signal display with colors
                signal_colors = {
                    "STRONG BUY": "🟢",
                    "BUY": "🟢",
                    "HOLD": "🟡",
                    "SELL": "🔴",
                    "STRONG SELL": "🔴",
                }

                st.success(
                    f"## {signal_colors.get(signal, '⚪')} Trading Signal: **{signal}**"
                )
                st.metric("Confidence Level", f"{confidence}/10", delta=None)

                # Display detailed analysis
                col3, col4 = st.columns(2)

                with col3:
                    st.subheader("✅ Key Reasons")
                    for reason in analysis.get("reasons", []):
                        st.write(f"• {reason}")

                with col4:
                    st.subheader("⚠️ Risk Factors")
                    for risk in analysis.get("risks", []):
                        st.write(f"• {risk}")

                st.subheader("📋 Summary")
                st.write(analysis.get("summary", "No summary available"))

            else:
                st.error(f"Analysis failed: {analysis}")

            # Display source data
            with st.expander("📰 View Source Articles"):
                if articles:
                    for i, article in enumerate(articles, 1):
                        st.write(f"**{i}. {article['title']}**")
                        st.write(f"Source: {article['source']}")
                        if article["url"]:
                            st.write(f"[Read more]({article['url']})")
                        st.write("---")
                else:
                    st.write("No articles found for this symbol.")

            with st.expander("📱 Social Sentiment Data"):
                for doc in insider_sentiments:
                    # print the json document
                    st.json(doc)

                for doc in analyst_sentiments:
                    # print the json document
                    st.json(doc)

    # Footer
    st.markdown("---")
    st.markdown(
        """
    **Disclaimer:** This tool is for educational purposes only. 
    Not financial advice. Always do your own research before making investment decisions.
    """
    )


if __name__ == "__main__":
    main()
