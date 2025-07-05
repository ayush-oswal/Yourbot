from fastapi import APIRouter, Depends, Request
from app.prisma.prisma_client import get_prisma
from app.middleware.get_user import get_current_user
from app.utils.rate_limiter import limiter

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/")
@limiter.limit("40/minute")
async def get_user(request: Request, user_data: dict = Depends(get_current_user)):
    Prisma = await get_prisma()
    user = await Prisma.user.find_unique(
        where={'id': user_data["user_id"]},
        include={
            "chatbots": True
        }
    )
    return user


