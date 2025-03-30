from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.prisma.prisma_client import Prisma
from app.middleware.get_user import get_current_user
import google.generativeai as genai
from app.constants.prompts import QUERY_MODIFICATION_INSTRUCTION
import os
import httpx
from fastapi.responses import StreamingResponse
from app.prisma.prisma_client import Prisma

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(model_name="gemini-2.5-pro-exp-03-25",system_instruction=QUERY_MODIFICATION_INSTRUCTION)

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
    # Create client with longer timeout
    async with httpx.AsyncClient(timeout=httpx.Timeout(300.0)) as client:
        try:
            async with client.stream(
                "POST",
                INFERENCE_SERVER_URL + "/infer",
                json={
                    "query": refined_query, 
                    "chatbot_id": chatbot_id, 
                    "previous_messages": previous_messages
                },
                headers={
                    "Accept": "text/event-stream",
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            ) as response:
                async for chunk in response.aiter_text():
                    if chunk:
                        yield chunk.encode('utf-8') 
        except httpx.ReadTimeout as e:
            print(f"Timeout error: {e}")
            yield b"Error: Request timed out"
        except Exception as e:
            print(f"Error during streaming: {e}")
            yield f"Error: {str(e)}".encode('utf-8')


            
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
    
