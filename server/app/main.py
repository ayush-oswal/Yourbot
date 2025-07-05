from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes.file_route import router as file_router
from app.routes.text_route import router as text_router
from app.routes.auth_route import router as auth_router
from app.routes.process_route import router as process_router
from app.routes.inference_route import router as inference_router
from app.routes.chatbot_route import router as chatbot_router
from app.routes.user_route import router as user_router
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

load_dotenv()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Include routers
app.include_router(file_router)
app.include_router(text_router)
app.include_router(auth_router)
app.include_router(process_router)
app.include_router(inference_router)
app.include_router(chatbot_router)
app.include_router(user_router)

@app.get("/")
@limiter.limit("40/minute")
def read_root(request: Request):
    return {"message": "Hello, brokie!"}