from fastapi import APIRouter, HTTPException, Depends, Request
from app.services.s3Client import generate_presigned_upload_url
from app.utils.filename import generate_unique_filename
from app.middleware.get_user import get_current_user
from app.prisma.prisma_client import get_prisma
from app.utils.rate_limiter import limiter


router = APIRouter(
    prefix="/text",
    tags=["text"]
)

@router.get("/")
@limiter.limit("40/minute")
async def get_text_upload_url(request: Request, user_data: dict = Depends(get_current_user)):
    """Generate a presigned URL and unique filename for text upload."""
    try:
        #check if user has tokens
        Prisma = await get_prisma()
        user = await Prisma.user.find_unique(where={"id": user_data["user_id"]})
        if user.tokens<=0 : 
            return {"message": "Not enough tokens"}
        if not user or not user.tokens:
            raise HTTPException(status_code=403, detail="User does not have valid tokens")
        key = generate_unique_filename("uploads/text", "txt")
        upload_url = generate_presigned_upload_url(key, "text/plain")
        return {"key": key, "upload_url": upload_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
