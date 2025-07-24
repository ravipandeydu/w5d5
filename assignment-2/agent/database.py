from langchain_community.utilities import SQLDatabase
from .config import DB_URI

# Initialize the SQLDatabase object once and reuse it
db = SQLDatabase.from_uri(DB_URI)