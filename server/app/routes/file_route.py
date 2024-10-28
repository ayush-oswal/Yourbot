from fastapi import APIRouter, HTTPException, Depends
from app.services.s3Client import generate_unique_filename, generate_presigned_upload_url
from app.middleware.get_user import get_current_user

router = APIRouter(
    prefix="/file",
    tags=["file"]
)

@router.get("/")
async def get_file_upload_url(extension: str = "pdf", user_data: dict = Depends(get_current_user)):
    """Generate a presigned URL and unique filename for file upload."""
    try:
        filename = generate_unique_filename("uploads/files", extension)
        upload_url = generate_presigned_upload_url(filename)
        return {"filename": filename, "upload_url": upload_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))