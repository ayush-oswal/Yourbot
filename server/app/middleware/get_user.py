from fastapi import Request, HTTPException, Depends
from app.utils.jwt import verify_jwt

async def get_current_user(request: Request):
    """Verify JWT from the Authorization header or cookies."""
    token = request.cookies.get("access_token")  # Check cookie
    if not token:
        auth_header = request.headers.get("Authorization")  # Fallback to header
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization token missing")

        token = auth_header.split(" ")[1]  # Extract token from header

    # Verify the token
    user_data = verify_jwt(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user_data  # Return the decoded user data
