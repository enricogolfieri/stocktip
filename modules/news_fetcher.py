"""Fetch news articles about the stock symbol"""

import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re


class NewsFetcher:
    def __init__(self, news_api_key=None):
        self.news_api_key = news_api_key

    def api_key_exists(self):
        """Check if NewsAPI key exists"""
        return self.news_api_key is not None and self.news_api_key != ""

    def fetch_news_api(self, symbol, days, max_articles=10):
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
                        if len(articles) >= max_articles:
                            break
                    return True, articles
        except Exception as e:
            return False, f"Error fetching news from NewsAPI: {str(e)}"

    def fetch_yahoo_finance_news(self, symbol, max_articles=10):
        articles = []

        # Extract news headlines and snippets
        url = f"https://finance.yahoo.com/quote/{symbol}/news?p={symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                news_items = soup.find_all(
                    "h3", {"class": re.compile(".*headline.*", re.I)}
                )
                for item in news_items[:max_articles]:
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
                return True, articles
            else:
                return (
                    False,
                    f"Error fetching news from Yahoo Finance: {response.status_code}",
                )
        except Exception as e:
            return False, f"Error fetching news from Yahoo Finance: {str(e)}"

    def fetch_finviz_news(self, symbol, max_articles=10):
        articles = []
        url = f"https://finviz.com/quote.ashx?t={symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return False, f"Error fetching news from Finviz: {response.status_code}"

            soup = BeautifulSoup(response.content, "html.parser")

            news_items = soup.find_all("a", {"class": "tab-link-news"})
            for item in news_items[:max_articles]:
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
            return True, articles
        except Exception as e:
            return False, f"Could not scrape from {url}: {str(e)}"
