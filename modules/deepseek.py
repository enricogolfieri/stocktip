from openai import OpenAI
import os
from enum import Enum


class DeepSeekModels(Enum):
    DEEPSEEK_CHAT = "deepseek-chat"
    DEEPSEEK_REASONER = "deepseek-reasoner"


class DeepSeek:
    def __init__(self, deepseek_api_key, deepseek_model=DeepSeekModels.DEEPSEEK_CHAT):
        """Initialize with DeepSeek API key"""
        self.deepseek_api_key = deepseek_api_key
        self.deepseek_model = deepseek_model

    def test_deepseek_api(self):
        """Test if DeepSeek API key is valid"""
        if not self.deepseek_api_key.exists():
            return "Error: DeepSeek API key not found in .env file"

        try:
            client = OpenAI(
                api_key=self.deepseek_api_key.value,
                base_url="https://api.deepseek.com",
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": "Test DeepSeek API"}],
                temperature=0.3,
                max_tokens=50,
            )
            return True, response.choices[0].message.content
        except Exception as e:
            return False, f"Error testing DeepSeek API: {str(e)}"

    def send(self, prompt, temperature=0.3, max_tokens=5000):
        client = OpenAI(
            api_key=self.deepseek_api_key.value, base_url="https://api.deepseek.com"
        )
        # Use r1
        response = client.chat.completions.create(
            model=self.deepseek_model.value,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
