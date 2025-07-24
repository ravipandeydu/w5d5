# agent/main_agent.py

from langchain_openai import ChatOpenAI  # <-- 1. IMPORT THE CORRECT CLASS
from langchain.agents import AgentExecutor
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.openai_tools.base import create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .config import OPENAI_API_KEY
from .database import db
from .tools import find_best_grocery_deal, set_agent_executor

def get_agent_executor():
    """
    Creates and returns the main SQL agent executor.
    """
    # 2. USE THE ChatOpenAI CLASS INSTEAD OF OpenAI
    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name="gpt-4")
    
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    sql_tools = sql_toolkit.get_tools()
    
    all_tools = sql_tools + [find_best_grocery_deal]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are an AI assistant that helps users find the best deals on groceries from a database.
        
        - You have access to a set of tools to query a database and to handle complex grocery lists.
        - For simple questions like 'cheapest onions?', query the database directly.
        - For complex lists like 'best deal for 1kg onions and 500g tomatoes under 1000', use the `find_best_grocery_deal` tool.
        - Always respond in a friendly, concise manner.
        - When providing final answers about prices, bold the price and platform. For example: The best price is **₹55.50** on **Blinkit**.
        """),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, all_tools, prompt)
    
    agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)
    
    set_agent_executor(agent_executor)
    
    return agent_executor