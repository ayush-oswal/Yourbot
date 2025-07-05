from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from app.middleware.get_user import get_current_user
# from app.services.redisClient import lpush_to_queue
from app.services.sqsClient import send_to_queue

from app.services.s3Client import generate_presigned_download_url
from app.prisma.prisma_client import get_prisma
from app.utils.rate_limiter import limiter

router = APIRouter(
    prefix="/process",
    tags=["process"]
)

class ProcessFileData(BaseModel):
    key: str
    chatbot_id: str

@router.post("/")
@limiter.limit("40/minute")
async def process_file(request: Request, data: ProcessFileData, user_data: dict = Depends(get_current_user)):
    """Process a file."""
    try:
        Prisma = await get_prisma()
        #code to check if user is owner of chatbot
        chatbot = await Prisma.chatbot.find_unique(
            where = {
                "id": data.chatbot_id,
                "userId": user_data["user_id"]
            }
        )
        if not chatbot:
            raise HTTPException(status_code=403, detail="You are not the owner of this chatbot")
        
        download_url = generate_presigned_download_url(data.key)
        message_id = send_to_queue("process_file", {**data.model_dump(), "download_url": download_url, "user_id": user_data["user_id"]})
        return {"message": "File processing started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
