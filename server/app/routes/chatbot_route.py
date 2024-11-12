from fastapi import APIRouter, HTTPException, Depends
from app.middleware.get_user import get_current_user
from app.prisma.prisma_client import Prisma
from pydantic import BaseModel

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"]
)

class ChatbotData(BaseModel):
    name: str
    description: str

@router.post("/create")
async def create_chatbot(data: ChatbotData, user_data: dict = Depends(get_current_user)):
    try:
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

