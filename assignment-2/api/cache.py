import redis
import json
from .main import agent_executor # Import the agent from the main API file
from agent.config import REDIS_HOST, REDIS_PORT

# Initialize Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

def get_cached_or_execute(query: str):
    """A cache-aside wrapper for the agent."""
    cache_key = f"qcommerce_query:{query.lower().strip()}"
    
    try:
        cached_result = redis_client.get(cache_key)
        if cached_result:
            print("--- Cache HIT ---")
            return json.loads(cached_result)
    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection error: {e}. Bypassing cache.")

    print("--- Cache MISS ---")
    response = agent_executor.invoke({"input": query})
    
    # Cache the result for 5 minutes (300 seconds)
    try:
        redis_client.set(cache_key, json.dumps(response), ex=300)
    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection error: {e}. Could not write to cache.")

    return response