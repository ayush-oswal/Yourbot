from fastapi import APIRouter, HTTPException, Depends
from app.prisma.prisma_client import get_prisma
from pydantic import BaseModel
from app.core.jina_ai import JinaAI

router = APIRouter()

class InferRequest(BaseModel):
    query: str
    chatbot_id: str
    previous_messages: list[str]

@router.post("/infer")
async def infer(request: InferRequest):
    print(request)
    # Prisma = await get_prisma()
    # get embedding of query, search pinecone index for similar docs top k, use chunk_id in metadata to obtain chunk text, then use groq to generate response
    jina_ai = JinaAI()
    embedding = jina_ai.fetch_embeddings(request.query)

    return {"message": "Hello, World!"}
