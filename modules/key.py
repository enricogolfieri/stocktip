from dotenv import load_dotenv
import os
import modules.logger as logger

# Load environment variables
load_dotenv()

keys = {}


def add_key(key):
    global keys
    if key.name in keys:
        raise ValueError(f"Key '{key.name}' already exists")
    keys[key.name] = key


def iterate_keys():
    """Iterate over all keys"""
    for _, key in keys.items():
        yield key


class Key:
    def __init__(self, name, description):
        global keys
        if name in keys:
            key = keys[name]
            self.name = key.name
            self.value = key.value
            self.description = key.description
            logger.info(f"Key '{name}' already exists, using existing value")
            return
        """Initialize with the name of the key"""
        self.name = name
        self.value = os.getenv(name)
        self.description = description
        if self.value is None:
            logger.warning(f"Key '{name}' not found in environment variables")
            self.value = ""
        else:
            logger.info(f"Key '{name}' loaded with value: {self.value_to_string()}")
        add_key(self)

    def exists(self):
        """Check if the key exists"""
        return self.value is not None and self.value != ""

    def value_to_string(self):
        """Return a string representation of the key value"""
        return self.value[:4] + "..." + self.value[-4:] if self.value else "Not set"


class DeepSeekKey(Key):
    def __init__(self):
        """Initialize with DeepSeek API key"""
        super().__init__("DEEPSEEK_API_KEY", "DeepSeek API")


class NewsAPIKey(Key):
    def __init__(self):
        """Initialize with NewsAPI key"""
        super().__init__("NEWS_API_KEY", "NewsAPI Key")
