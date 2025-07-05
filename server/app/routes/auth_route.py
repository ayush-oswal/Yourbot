from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel
from app.utils.jwt import create_jwt
from app.prisma.prisma_client import get_prisma
from jose import jwt, JWTError
from app.utils.rate_limiter import limiter
import os

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class LoginData(BaseModel):
    token: str

@router.post("/login")
@limiter.limit("40/minute")
async def login(request: Request, data: LoginData, response: Response):
    """Login or register user and set JWT cookie."""
    try:
        nextauth_secret = os.getenv("NEXTAUTH_SECRET")
        if not nextauth_secret:
            raise HTTPException(status_code=500, detail="NextAuth secret not configured")

        try:
            payload = jwt.decode(data.token, nextauth_secret)
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid NextAuth token")


        email = payload.get('email')
        name = payload.get('name')
        
        if not email:
            raise HTTPException(status_code=401, detail="No email in token")

        Prisma = await get_prisma()

        user = await Prisma.user.find_unique(
            where={'email': email}
        )
        
        if not user:
            user = await Prisma.user.create(
                data={
                    'email': email,
                    'username': name
                }
            )
        
        token = create_jwt({"user_id": user.id})
        
        return {
            "message": "Successfully logged in",
            "user_id": user.id,
            "token": token
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
