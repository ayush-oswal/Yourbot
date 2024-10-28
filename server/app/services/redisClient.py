import os
import redis
import json

# Initialize Redis client with URL from environment variable
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")  # Default fallback for local Redis
redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

def lpush_to_queue(queue_name: str, message: dict):
    """Push a message to a Redis list (queue)."""
    try:
        # Convert the message to a JSON string and push to Redis list
        redis_client.lpush(queue_name, json.dumps(message))
        print(f"Message pushed to queue: {queue_name}")
    except Exception as e:
        raise RuntimeError(f"Failed to push message to queue: {str(e)}")

# Example function to check Redis connection (optional)
def ping_redis():
    try:
        return redis_client.ping()
    except redis.ConnectionError:
        raise RuntimeError("Failed to connect to Redis.")
