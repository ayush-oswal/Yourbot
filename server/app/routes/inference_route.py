from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.prisma.prisma_client import Prisma
from app.middleware.get_user import get_current_user
import google.generativeai as genai
from app.constants.prompts import QUERY_MODIFICATION_INSTRUCTION
import os
import httpx
from fastapi.responses import StreamingResponse

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",system_instruction=QUERY_MODIFICATION_INSTRUCTION)

INFERENCE_SERVER_URL = os.getenv("INFERENCE_SERVER_URL") or "http://localhost:8001"

router = APIRouter(
    prefix="/inference",
    tags=["inference"]
)

class InferenceData(BaseModel):
    chatbot_id: str
    query: str
    previous_messages: list[dict]

class ExternalInferenceData(BaseModel):
    chatbot_id: str
    query: str
    previous_messages: list[dict]
    api_key: str

async def get_answer(chatbot_id: str, query: str, previous_messages: list[dict]):
    refined_query = model.generate_content(query).text
    print(refined_query)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            INFERENCE_SERVER_URL + "/infer",
            json={"query": refined_query, "chatbot_id": chatbot_id, "previous_messages": previous_messages},
            headers={"Accept": "text/event-stream"},
            stream=True
        )
        async for chunk in response.aiter_bytes():
            yield chunk

            
@router.post("/")
async def inference(data: InferenceData, user_data: dict = Depends(get_current_user)):
    chatbot = await Prisma.chatbot.find_unique(where={"id": data.chatbot_id, "userId": user_data["user_id"]})
    if not chatbot:
        raise HTTPException(status_code=403, detail="You are not the owner of this chatbot")
    
    # call the inference server route here with post
    return StreamingResponse(get_answer(chatbot_id=data.chatbot_id, query=data.query, previous_messages=data.previous_messages), media_type="text/event-stream")
    
    
@router.post("/external")
async def external_inference(data: ExternalInferenceData):
    # Fetch user with api key and check if they have access to the chatbot
    user = await Prisma.user.find_unique(where={"apiKey": data.api_key}, include={"chatbots": True})
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API key") 
    # check if the chatbot exists and the user has access to it
    chatbot = None
    for c in user.chatbots:
        if c.id == data.chatbot_id:
            chatbot = c
            break
    if not chatbot:
        raise HTTPException(status_code=403, detail="You do not have access to this chatbot")
    
    # call the inference server route here with post
    return StreamingResponse(get_answer(chatbot_id=data.chatbot_id, query=data.query, previous_messages=data.previous_messages), media_type="text/event-stream")
    
