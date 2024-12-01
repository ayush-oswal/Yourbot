import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

Index = pc.Index("yourbot")

async def get_matches(embedding, chatbot_id, top_k=10):
    response = Index.query(
        vector=embedding,
        filter={"chatbot_id": {"$eq": chatbot_id}},
        top_k=top_k,
        include_metadata=True
    )
    print(response)
    return response["matches"]
