import os
import redis
import json

# Initialize Redis client with URL from environment variable
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")  # Default fallback for local Redis
redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

def lpush_to_queue(queue_name: str, message: dict):
    """Push a message to a Redis list (queue)."""
    try:
        json_message = json.dumps(message)
        print(f"Pushing message to queue {queue_name}: {json_message}")
        redis_client.lpush(queue_name, json_message)
        queue_length = redis_client.llen(queue_name)
        print(f"Queue {queue_name} length after push: {queue_length}")
        return True
    except Exception as e:
        print(f"Failed to push message to queue: {str(e)}")
        raise RuntimeError(f"Failed to push message to queue: {str(e)}")

# Example function to check Redis connection (optional)
def ping_redis():
    try:
        return redis_client.ping()
    except redis.ConnectionError:
        raise RuntimeError("Failed to connect to Redis.")
