import os
import requests
from dotenv import load_dotenv
import random

load_dotenv()

class JinaAI:
    def __init__(self):
        pass
    
    def get_random_jina_api_key(self):
        count = int(os.getenv("NUMBER_OF_API_KEYS_JINA_AI"))
        random_index = random.randint(1, count)
        jina_api_key = os.getenv(f"JINA_API_KEY_{random_index}") or os.getenv("JINA_API_KEY_1")
        return jina_api_key
    
    def fetch_embeddings(self, query: str):
        jina_api_key = self.get_random_jina_api_key()
        url = "https://api.jina.ai/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jina_api_key}"
        }
        data = {
            "model": "jina-embeddings-v3",
            "task": "text-matching",
            "dimensions": 1024,
            "late_chunking": False,
            "embedding_type": "float",
            "input": query
        }
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        embedding = response_data.get("data", [{}])[0].get("embedding", [])
        return embedding
