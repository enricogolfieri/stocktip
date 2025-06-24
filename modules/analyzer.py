import json


class StockAnalyzer:
    def __init__(self, ai_engine):
        """Initialize with DeepSeek API key"""
        self.ai_engine = ai_engine

    def prompt(self, symbol, content):
        return f"""
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

    def analyze(self, symbol, articles: list, social_data: list):
        """Use AI engine to analyze the collected data and provide trading signal"""

        if not self.ai_engine:
            return "Error: AI engine not initialized"

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

        prompt = self.prompt(symbol, content)

        try:
            response = self.ai_engine.send(prompt)
            # Try to parse JSON response
            try:
                # Extract JSON from the response
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                if json_start != -1 and json_end != -1:
                    json_str = response[json_start:json_end]
                    return json.loads(json_str)
                else:
                    # Fallback if JSON parsing fails
                    return {
                        "signal": "HOLD",
                        "confidence": 5,
                        "reasons": ["Analysis completed but format error occurred"],
                        "risks": ["Unable to parse detailed analysis"],
                        "summary": response[:500],
                    }
            except json.JSONDecodeError:
                return {
                    "signal": "UNKNOWN",
                    "confidence": 0,
                    "reasons": ["Analysis completed but JSON parsing failed"],
                    "risks": ["Format error in AI response"],
                    "summary": response[:500],
                }

        except Exception as e:
            return {
                "signal": "ERROR",
                "confidence": 0,
                "reasons": [f"Error during analysis: {str(e)}"],
                "risks": ["API error or connection issue"],
                "summary": str(e),
            }
