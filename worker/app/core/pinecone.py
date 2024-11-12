from pinecone import Pinecone
import os
import dotenv   

dotenv.load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index("yourbot")