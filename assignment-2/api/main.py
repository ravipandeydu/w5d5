from fastapi import FastAPI, Request
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from agent.main_agent import get_agent_executor

# --- Initialization ---
# Create the agent executor once when the app starts
agent_executor = get_agent_executor()

# Setup rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Quick Commerce SQL Agent API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
@limiter.limit("15/minute")
async def handle_query(request: Request, body: QueryRequest):
    """
    Receives a natural language query, processes it with the agent, and returns the result.
    """
    # Note: For simplicity, we are not using the Redis cache here.
    # To enable it, you would call `get_cached_or_execute(body.query)`
    # from the `api.cache` module.
    
    response = agent_executor.invoke({"input": body.query})
    return {"response": response.get('output')}