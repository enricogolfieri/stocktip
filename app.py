import streamlit as st
import requests
import os
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import time
from bs4 import BeautifulSoup
import re

# Load environment variables
load_dotenv()


class StockAnalyzer:
    def __init__(self):
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        self.news_api_key = os.getenv(
            "NEWS_API_KEY"
        )  # Optional: for better news sources

    def get_news_articles(self, symbol, days=7):
        """Fetch news articles about the stock symbol"""
        articles = []

        try:
            # Method 1: Using NewsAPI (if API key is provided)
            if self.news_api_key:
                url = f"https://newsapi.org/v2/everything"
                params = {
                    "q": f"{symbol} stock OR {symbol} earnings OR {symbol} company",
                    "from": (datetime.now() - timedelta(days=days)).strftime(
                        "%Y-%m-%d"
                    ),
                    "sortBy": "relevancy",
                    "language": "en",
                    "pageSize": 10,
                    "apiKey": self.news_api_key,
                }

                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for article in data.get("articles", []):
                        if article.get("title") and article.get("description"):
                            articles.append(
                                {
                                    "title": article["title"],
                                    "content": article["description"],
                                    "url": article.get("url", ""),
                                    "source": "NewsAPI",
                                }
                            )

            # Method 2: Web scraping from financial news sites
            search_urls = [
                f"https://finance.yahoo.com/quote/{symbol}/news/",
                f"https://finviz.com/quote.ashx?t={symbol}",
            ]

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            for url in search_urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")

                        # Extract news headlines and snippets
                        if "yahoo.com" in url:
                            news_items = soup.find_all(
                                "h3", {"class": re.compile(".*headline.*", re.I)}
                            )
                            for item in news_items[:5]:
                                title = item.get_text(strip=True)
                                if title and len(title) > 10:
                                    articles.append(
                                        {
                                            "title": title,
                                            "content": title,
                                            "url": url,
                                            "source": "Yahoo Finance",
                                        }
                                    )

                        elif "finviz.com" in url:
                            news_items = soup.find_all("a", {"class": "tab-link-news"})
                            for item in news_items[:5]:
                                title = item.get_text(strip=True)
                                if title and len(title) > 10:
                                    articles.append(
                                        {
                                            "title": title,
                                            "content": title,
                                            "url": item.get("href", ""),
                                            "source": "Finviz",
                                        }
                                    )

                except Exception as e:
                    st.warning(f"Could not scrape from {url}: {str(e)}")
                    continue

        except Exception as e:
            st.error(f"Error fetching news: {str(e)}")

        return articles[:15]  # Limit to 15 articles

    def get_social_sentiment(self, symbol):
        # TODO - Implement social media sentiment analysis
        return []

    def analyze_with_deepseek(self, symbol, articles, social_data):
        """Use DeepSeek to analyze the collected data and provide trading signal"""

        if not self.deepseek_api_key:
            return "Error: DeepSeek API key not found in .env file"

        # Prepare the content for analysis
        content = f"Stock Symbol: {symbol}\n\n"
        content += "Recent News Articles:\n"
        for i, article in enumerate(articles, 1):
            content += f"{i}. {article['title']}\n"
            if article["content"] != article["title"]:
                content += f"   {article['content'][:200]}...\n"
            content += f"   Source: {article['source']}\n\n"

        content += "\nSocial Media Sentiment:\n"
        for i, social in enumerate(social_data, 1):
            content += f"{i}. {social}\n"

        prompt = f"""
        As a financial analyst, analyze the following information about {symbol} stock and provide a trading recommendation.
        
        {content}
        
        Based on this information, provide:
        1. A trading signal: STRONG BUY, BUY, HOLD, SELL, or STRONG SELL
        2. A confidence level (1-10)
        3. Key reasons for your recommendation (2-3 bullet points)
        4. Risk factors to consider
        
        Please be objective and consider both positive and negative factors.
        Format your response as JSON with the following structure:
        {{
            "signal": "STRONG BUY/BUY/HOLD/SELL/STRONG SELL",
            "confidence": 1-10,
            "reasons": ["reason1", "reason2", "reason3"],
            "risks": ["risk1", "risk2"],
            "summary": "Brief explanation of the recommendation"
        }}
        """

        try:
            # Use OpenAI-compatible format for DeepSeek
            try:
                from openai import OpenAI

                client = OpenAI(
                    api_key=self.deepseek_api_key, base_url="https://api.deepseek.com"
                )

                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=1000,
                )

                ai_response = response.choices[0].message.content

            except ImportError:
                # Fallback to requests if openai library not available
                st.warning("OpenAI library not found. Install with: pip install openai")

                url = "https://api.deepseek.com/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.deepseek_api_key}",
                    "Content-Type": "application/json",
                }

                data = {
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 1000,
                }

                response = requests.post(url, headers=headers, json=data, timeout=30)

                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                else:
                    return f"Error: DeepSeek API returned status {response.status_code}. Response: {response.text}"

            # Try to parse JSON response
            try:
                # Extract JSON from the response
                json_start = ai_response.find("{")
                json_end = ai_response.rfind("}") + 1
                if json_start != -1 and json_end != -1:
                    json_str = ai_response[json_start:json_end]
                    return json.loads(json_str)
                else:
                    # Fallback if JSON parsing fails
                    return {
                        "signal": "HOLD",
                        "confidence": 5,
                        "reasons": ["Analysis completed but format error occurred"],
                        "risks": ["Unable to parse detailed analysis"],
                        "summary": ai_response[:500],
                    }
            except json.JSONDecodeError:
                return {
                    "signal": "HOLD",
                    "confidence": 5,
                    "reasons": ["Analysis completed but JSON parsing failed"],
                    "risks": ["Format error in AI response"],
                    "summary": ai_response[:500],
                }

        except Exception as e:
            return f"Error calling DeepSeek API: {str(e)}"


def main():
    st.set_page_config(
        page_title="Stock Sentiment Analyzer", page_icon="📈", layout="wide"
    )

    st.title("📈 Stock Sentiment Analyzer")
    st.subheader("AI-Powered Trading Signals Using DeepSeek")

    # Sidebar for configuration
    st.sidebar.header("Configuration")

    # API key status check
    analyzer_temp = StockAnalyzer()
    if analyzer_temp.deepseek_api_key:
        st.sidebar.success("✅ DeepSeek API key loaded")
        st.sidebar.text(
            analyzer_temp.deepseek_api_key[:4]
            + "..."
            + analyzer_temp.deepseek_api_key[-4:]
        )
    else:
        st.sidebar.error("❌ DeepSeek API key missing")
    if analyzer_temp.news_api_key:
        st.sidebar.success("✅ NewsAPI key loaded")
        st.sidebar.text(
            analyzer_temp.news_api_key[:4] + "..." + analyzer_temp.news_api_key[-4:]
        )
    else:
        st.sidebar.warning("⚠️ NewsAPI key not found. Some news sources may be limited.")

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
            analyzer = StockAnalyzer()

            # Check if API key is available
            if not analyzer.deepseek_api_key:
                st.error(
                    "❌ DeepSeek API key not found! Please add DEEPSEEK_API_KEY to your .env file."
                )
                st.stop()

            with st.spinner(f"Analyzing {symbol}..."):
                # Fetch data
                st.info("📰 Fetching news articles...")
                articles = analyzer.get_news_articles(symbol, days)

                st.info("📱 Analyzing social sentiment...")
                social_data = analyzer.get_social_sentiment(symbol)

                st.info("🤖 Getting AI analysis from DeepSeek...")
                analysis = analyzer.analyze_with_deepseek(symbol, articles, social_data)

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
                for i, social in enumerate(social_data, 1):
                    st.write(f"{i}. {social}")

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
