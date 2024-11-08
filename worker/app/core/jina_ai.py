import os
import random
from dotenv import load_dotenv
import requests

url = "https://api.jina.ai/v1/embeddings"

load_dotenv()



class JinaAI:
    def __init__(self): 
        pass

    def get_random_jina_api_key(self):
        count = os.getenv("NUMBER_OF_API_KEYS_JINA_AI")
        random_index = random.randint(1, count)
        jina_api_key = os.getenv(f"JINA_API_KEY_{random_index}")
        return jina_api_key
    
    def fetch_embeddings(self, chunks, batch_size=4):
        print(f"Fetching embeddings for {len(chunks)} chunks")
        # jina_api_key = self.get_random_jina_api_key()
        jina_api_key = "jina_fcc1305fd47641bc85f626fdcc049bdfi3gxrnbzsiSm34xdOKXCh7qdIWA1"
        url = "https://api.jina.ai/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jina_api_key}"
        }
        results = []
        total_tokens = 0  # Initialize total tokens counter
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            data = {
                "model": "jina-embeddings-v3",
                "task": "text-matching",
                "dimensions": 1024,
                "late_chunking": False,
                "embedding_type": "float",
                "input": batch
            }
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            results.extend(response_data.get('data', []))
            total_tokens += response_data.get('usage', {}).get('total_tokens', 0)  # Accumulate total tokens
        return results, total_tokens
        
