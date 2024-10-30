from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.middleware.get_user import get_current_user
from app.services.redisClient import lpush_to_queue
from app.services.s3Client import generate_presigned_download_url

router = APIRouter(
    prefix="/process",
    tags=["process"]
)

class ProcessFileData(BaseModel):
    key: str
    chatbot_id: str

@router.post("/")
async def process_file(data: ProcessFileData, user_data: dict = Depends(get_current_user)):
    """Process a file."""
    try:
        download_url = generate_presigned_download_url(data.key)
        lpush_to_queue("process_file", {**data.model_dump(), "download_url": download_url, "user_id": user_data["user_id"]})
        return {"message": "File processing started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
