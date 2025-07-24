🛒 Quick Commerce SQL Agent
This project is an intelligent price comparison platform for quick commerce apps like Blinkit, Zepto, and Instamart. It uses a sophisticated AI agent powered by LangChain and OpenAI to understand natural language queries, interact with a SQL database, and find the best deals on thousands of products in real-time.

✨ Features
Natural Language Queries: Ask complex questions like "Which app has the cheapest onions?" or "Find the best deals for a ₹1000 grocery list."

Multi-Platform Comparison: Tracks and compares real-time pricing and availability across multiple quick commerce platforms.

Intelligent SQL Agent: Uses LangChain and an OpenAI model (GPT-4) to dynamically generate and execute SQL queries.

Custom Tooling: Handles complex, multi-step logic (like budget-based grocery lists) that a simple SQL query cannot solve.

Data-Driven: Populated with real-world datasets from Kaggle, which are automatically cleaned and loaded into a local SQLite database.

Web Interface: A user-friendly UI built with Streamlit for easy interaction with the agent.

Scalable Backend: A robust backend API built with FastAPI, including security features like rate limiting.

🛠️ Tech Stack
Backend: Python, FastAPI

Frontend: Streamlit

AI/LLM: LangChain, OpenAI (GPT-4)

Database: SQLite

Data Handling: Pandas

API Security: SlowAPI (for rate limiting)

📂 Project Structure
The project is organized into modular directories for clarity and scalability:

q-commerce-agent/
├── db/
│   ├── schema.sql
│   └── populate_data.py
├── agent/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main_agent.py
│   └── tools.py
├── api/
│   ├── __init__.py
│   ├── cache.py
│   └── main.py
├── ui/
│   ├── __init__.py
│   └── app.py
├── .env.example
├── requirements.txt
└── README.md

🚀 Getting Started
Follow these steps to set up and run the project on your local machine.

Prerequisites
Make sure you have the following installed:

Python 3.9+

A code editor like VS Code

1. Clone the Repository
git clone <your-repo-url>
cd q-commerce-agent

2. Set Up a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.

# Create the virtual environment
python -m venv .venv

# Activate it (Windows)
.\.venv\Scripts\activate

# Activate it (macOS/Linux)
source .venv/bin/activate

3. Configure Environment Variables
You need to provide your OpenAI API key for the agent to work.

Copy the example .env file:

cp .env.example .env

Get an OpenAI API Key:

Go to https://platform.openai.com/account/api-keys.

Click + Create new secret key, copy it.

Update the .env file: Open the .env file and paste your new API key.

# .env
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxx"
DB_FILE_PATH="quick_commerce.db"

4. Install Dependencies
Install all the required Python packages using pip.

pip install -r requirements.txt

5. Prepare the Datasets
Download your datasets (e.g., from Kaggle).

Place the CSV files inside the data/ directory.

Ensure the filenames match those in db/populate_data.py (e.g., blinkit_data.csv, zepto_data.csv).

6. Set Up the Database
Run the population script. This will automatically:

Create the SQLite database file (quick_commerce.db).

Create the necessary tables from db/schema.sql.

Read your CSV files from the data/ directory.

Clean the data (handle missing values, format prices, etc.).

Load the clean data into the database.

python db/populate_data.py

▶️ Running the Application
The application consists of two parts: the backend API and the frontend UI. You need to run them in two separate terminals.

Terminal 1: Start the Backend API
Make sure your virtual environment is active in this terminal.

uvicorn api.main:app --reload

You should see a message indicating that the Uvicorn server is running on http://127.0.0.1:8000.

Terminal 2: Start the Frontend UI
Open a new terminal and activate the virtual environment again.

# Activate on Windows
.\.venv\Scripts\activate

# Activate on macOS/Linux
source .venv/bin/activate

# Run the Streamlit app
streamlit run ui/app.py

Streamlit will provide a URL (usually http://localhost:8501). Open this URL in your web browser to use the application.

💡 How to Use
Open the Streamlit URL in your browser.

Type a question into the text box. You can ask simple questions or more complex ones.

Click one of the example buttons to auto-fill the text box with a sample query.

Click the "🔍 Find Deals" button.

The agent's response will appear below. The backend terminal will show the agent's thought process and the SQL queries it generates.

🔧 Troubleshooting
ModuleNotFoundError: If you see this error, it means a required package is missing. Make sure your virtual environment is active and run pip install -r requirements.txt.

openai.AuthenticationError: This means your OpenAI API key is invalid or missing. Double-check your .env file and ensure the key is correct.

KeyError during data population: This means the column names in your CSV files do not match the COLUMN_MAPPINGS in db/populate_data.py. Update the dictionary to match your dataset's schema.

Encoding Errors (UnicodeDecodeError): If you get an error about 'utf-8' or another codec, it means your CSV has special characters. The populate_data.py script uses encoding='latin1', which is robust, but you can try other encodings like windows-1252 if needed.