import os
from jose import jwt, JWTError

# Load secret key and algorithm
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
JWT_ALGORITHM = "HS256"

def create_jwt(data: dict) -> str:
    """Generate a JWT for the given data."""
    token = jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def verify_jwt(token: str) -> dict:
    """Verify the JWT and return the payload if valid."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None  # Invalid or expired token
