from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from app.utils.jwt import create_jwt
from app.prisma.prisma_client import Prisma

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class LoginData(BaseModel):
    email: str
    name: str

@router.post("/login")
async def login(data: LoginData, response: Response):
    """Login or register user and set JWT cookie."""
    try:
        # Try to find existing user
        user = await Prisma.user.find_unique(
            where={'email': data.email}
        )
        
        # If user doesn't exist, create new user
        if not user:
            user = await Prisma.user.create(
                data={
                    'email': data.email,
                    'username': data.name
                }
            )
        
        # Create JWT with user ID
        token = create_jwt({"user_id": user.id})
        
        # Return token in response
        return {
            "message": "Successfully logged in",
            "user_id": user.id,
            "token": token
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
