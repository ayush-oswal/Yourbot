from fastapi import APIRouter, HTTPException, Depends, Query
from app.middleware.get_user import get_current_user
from app.prisma.prisma_client import get_prisma
from pydantic import BaseModel

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"]
)

class ChatbotData(BaseModel):
    name: str
    description: str

class ChatbotEditData(BaseModel):
    chatbot_id: str
    name: str
    description: str


@router.get("/{chatbot_id}")
async def get_chatbots(chatbot_id: str, user_data: dict = Depends(get_current_user)):
    try:
        Prisma = await get_prisma()
        chatbot = await Prisma.chatbot.find_first(
            where={"userId": user_data["user_id"], "id": chatbot_id}
        )
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        return chatbot
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create")
async def create_chatbot(data: ChatbotData, user_data: dict = Depends(get_current_user)):
    try:
        Prisma = await get_prisma()
        chatbot = await Prisma.chatbot.create(
            data = {
                "name": data.name,
                "description": data.description,
                "userId": user_data["user_id"]
            }
        )
        return {"chatbot_id": chatbot.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/edit")
async def edit_chatbot(data: ChatbotEditData, user_data: dict = Depends(get_current_user)):
    try:
        Prisma = await get_prisma()
        chatbot = await Prisma.chatbot.find_first(
            where = {"id": data.chatbot_id, "userId": user_data["user_id"]}
        )
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
        await Prisma.chatbot.update(
            where = {"id": data.chatbot_id},
            data = {"name": data.name, "description": data.description}
        )
        return {"message": "Chatbot updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{chatbot_id}/queries")
async def get_chatbot_queries(chatbot_id: str, page_number: int = Query(default=1), user_data: dict = Depends(get_current_user)):
    try:
        Prisma = await get_prisma()
        chatbot = await Prisma.chatbot.find_first(
            where={
                "id": chatbot_id,
                "userId": user_data["user_id"]
            }
        )
        
        if not chatbot:
            raise HTTPException(status_code=404, detail="Chatbot not found")
            
        total_count = await Prisma.queries.count(
            where={
                "chatbotId": chatbot_id
            }
        )
        
        queries = await Prisma.queries.find_many(
            where={
                "chatbotId": chatbot_id
            },
            skip=(page_number - 1) * 15,
            take=15,
            order={"createdAt": "desc"}
        )
        
        return {"total_count": total_count, "queries": queries}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
