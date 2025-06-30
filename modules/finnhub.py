import finnhub as finnhub


class Finnhub:
    """
    A class to interact with the Finnhub API for financial data analysis.
    """

    def __init__(self, key):
        """
        Initialize the Finnhub client with the provided API key.
        """
        self.finnhub_client = finnhub.Client(api_key=key.value)

    def get_stock_insider_transactions(self, symbol, from_date, to_date):
        """
        Fetch insider transactions for a given stock symbol within a date range.

        :param symbol: Stock symbol to fetch insider transactions for.
        :param from_date: Start date for the transactions (YYYY-MM-DD).
        :param to_date: End date for the transactions (YYYY-MM-DD).
        :return: List of insider transactions.
        """
        try:
            transactions = self.finnhub_client.stock_insider_transactions(
                symbol, from_date, to_date
            )
            return True, transactions
        except Exception as e:
            return False, f"Error fetching insider transactions: {str(e)}"

    def get_stock_insider_sentiment(self, symbol, from_date, to_date):
        """
        Fetch insider sentiment for a given stock symbol within a date range.

        :param symbol: Stock symbol to fetch insider sentiment for.
        :param from_date: Start date for the sentiment (YYYY-MM-DD).
        :param to_date: End date for the sentiment (YYYY-MM-DD).
        :return: Insider sentiment data.
        """
        try:
            sentiment = self.finnhub_client.stock_insider_sentiment(
                symbol, from_date, to_date
            )
            return True, sentiment
        except Exception as e:
            return False, f"Error fetching insider sentiment: {str(e)}"

    def get_stock_recommendations_trends(self, symbol):
        """
        Fetch stock recommendations trends for a given stock symbol.

        :param symbol: Stock symbol to fetch recommendations trends for.
        :return: Recommendations trends data.
        """
        try:
            trends = self.finnhub_client.recommendation_trends(symbol)
            return True, trends
        except Exception as e:
            return False, f"Error fetching recommendations trends: {str(e)}"
