from fastapi import APIRouter, HTTPException, Depends
from app.prisma.prisma_client import Prisma
from app.middleware.get_user import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/")
async def get_user(user_data: dict = Depends(get_current_user)):
    user = await Prisma.user.find_unique(
        where={'id': user_data["user_id"]},
        include={
            "chatbots": True
        }
    )
    return user


