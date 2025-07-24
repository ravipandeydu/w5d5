import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Database ---
# The DB_URI for SQLite is 'sqlite:///path/to/your/database.db'
DB_FILE_PATH = os.getenv("DB_FILE_PATH", "quick_commerce.db")
DB_URI = f"sqlite:///{DB_FILE_PATH}"

# --- Redis ---
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))