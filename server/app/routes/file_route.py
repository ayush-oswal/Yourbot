from fastapi import APIRouter, HTTPException, Depends
from app.services.s3Client import generate_presigned_upload_url
from app.utils.filename import generate_unique_filename
from app.middleware.get_user import get_current_user

router = APIRouter(
    prefix="/file",
    tags=["file"]
)

@router.get("/")
async def get_file_upload_url(extension: str = "pdf", user_data: dict = Depends(get_current_user)):
    """Generate a presigned URL and unique filename for file upload."""
    try:
        key = generate_unique_filename("uploads/files", extension)
        upload_url = generate_presigned_upload_url(key, "application/pdf")
        return {"key": key, "upload_url": upload_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))