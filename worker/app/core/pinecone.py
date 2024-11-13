from pinecone import Pinecone
import os
import dotenv   

dotenv.load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

Index = pc.Index("yourbot")

async def upsert_chunks(chunk_ids, embeddings, chatbot_id):
    try:
        Index.delete(delete_all=True)
        vectors_to_upsert = [{
            'id': str(chunk_ids[i]),
            'values': embeddings[i]['embedding'],
            'metadata': {"chatbot_id": str(chatbot_id), "chunk_id": str(chunk_ids[i])}
        } for i in range(len(embeddings))]
        
        # Batch upsert instead of individual upserts
        response = Index.upsert(
            vectors=vectors_to_upsert
        )
        print(f"Successfully upserted {len(vectors_to_upsert)} vectors to Pinecone")
        return response
    except Exception as e:
        print(f"Error upserting to Pinecone: {str(e)}")
        raise e

