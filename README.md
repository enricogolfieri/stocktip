# 📈 Stock Sentiment Analyzer

An AI-powered stock analysis tool that combines web scraping, sentiment analysis, and advanced AI reasoning to provide trading signals. Built with Streamlit and powered by DeepSeek AI.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![DeepSeek](https://img.shields.io/badge/AI-DeepSeek-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Features

- **Real-time News Scraping**: Automatically fetches latest news from Yahoo Finance, Finviz, and NewsAPI
- **AI-Powered Analysis**: Uses DeepSeek AI to analyze sentiment and market conditions
- **Trading Signals**: Provides clear recommendations (STRONG BUY, BUY, HOLD, SELL, STRONG SELL)
- **Confidence Scoring**: Shows AI confidence level (1-10) for each recommendation
- **Risk Assessment**: Identifies key risks and opportunities
- **Multi-Source Data**: Combines news articles and social sentiment analysis
- **Interactive UI**: Clean, responsive Streamlit interface
- **Cost Effective**: Uses DeepSeek API (~$0.14 per 1M tokens)


## 📋 Prerequisites

- Python 3.8 or higher
- DeepSeek API key (free tier available)
- NewsAPI key (optional, for enhanced news sources)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/enricogolfieri/stocktip.git
cd stocktip
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API keys
DEEPSEEK_API_KEY=your_deepseek_api_key_here
NEWS_API_KEY=your_news_api_key_here  # Optional
```

## 🔑 API Keys Setup

### DeepSeek API Key (Required)
1. Visit [DeepSeek Platform](https://platform.deepseek.com/api_keys)
2. Sign up for a free account
3. Create a new API key
4. Copy the key to your `.env` file

**Cost**: ~$0.14 per 1M input tokens, ~$0.28 per 1M output tokens

### NewsAPI Key (Optional)
1. Visit [NewsAPI](https://newsapi.org/)
2. Get a free API key (500 requests/day)
3. Add to your `.env` file for enhanced news coverage

## 🚀 Usage

1. **Start the application**
```bash
streamlit run app.py
```

or 

```
./run.sh
```

2. **Open your browser**
   - Navigate to `http://localhost:8501`

3. **Analyze a stock**
   - Enter a stock symbol (e.g., AAPL, TSLA, GOOGL)
   - Select analysis period (1-30 days)
   - Click "🔍 Analyze Stock"

4. **Review results**
   - View trading signal and confidence level
   - Read AI reasoning and risk factors
   - Examine source articles and data


## 🔧 Configuration Options

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | Yes | Your DeepSeek API key for AI analysis |
| `NEWS_API_KEY` | No | NewsAPI key for enhanced news sources |

### App Settings

- **Analysis Period**: 1-30 days of historical news
- **Temperature**: AI creativity level (0.3 for consistent results)
- **Max Tokens**: Response length limit (1000 tokens)

## 🛡️ Error Handling

### Common Issues

**401 Authentication Error**
```bash
# Check your API key
echo $DEEPSEEK_API_KEY

# Regenerate key if needed
# Visit platform.deepseek.com
```

**No Articles Found**
- Try different stock symbols
- Check if NewsAPI key is valid
- Some symbols may have limited coverage

**Rate Limiting**
- DeepSeek: No hard limits on official API
- NewsAPI: 500 requests/day on free tier

## 📊 Supported Data Sources

### News Sources
- **Yahoo Finance**: Real-time financial news
- **Finviz**: Market analysis and headlines
- **NewsAPI**: Global news coverage (with API key)

### Analysis Capabilities
- **Sentiment Analysis**: Positive/negative/neutral sentiment scoring
- **Market Context**: Economic and sector-specific analysis
- **Risk Assessment**: Identification of potential risks and opportunities
- **Technical Factors**: Integration of market trends and patterns

## 🔮 Roadmap

- [ ] Real Twitter/X integration
- [ ] Technical indicator analysis
- [ ] Portfolio tracking
- [ ] Email/SMS alerts
- [ ] Historical performance tracking
- [ ] Multiple AI model comparison
- [ ] Options and crypto support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🙏 Acknowledgments

- [DeepSeek](https://www.deepseek.com/) for providing affordable AI API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [NewsAPI](https://newsapi.org/) for news data
- Financial data providers (Yahoo Finance, Finviz)

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/stock-sentiment-analyzer/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/stock-sentiment-analyzer/discussions)
- 📧 **Email**: enrico.golfieri@gmail.com

---

**Made with ❤️** | Star ⭐ this repo if you found it useful!