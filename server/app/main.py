from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.file_route import router as file_router
from app.routes.text_route import router as text_router
from app.routes.auth_route import router as auth_router
from app.routes.process_route import router as process_router
from app.routes.inference_route import router as inference_router
from app.routes.chatbot_route import router as chatbot_router
from contextlib import asynccontextmanager
from app.prisma.prisma_client import Prisma
import os
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Connecting to Prisma...")
    await Prisma.connect()
    print("Connected to Prisma.")
    yield
    # Shutdown
    print("Disconnecting from Prisma...")
    await Prisma.disconnect()
    print("Disconnected from Prisma.")

app = FastAPI(lifespan=lifespan)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Include routers
app.include_router(file_router)
app.include_router(text_router)
app.include_router(auth_router)
app.include_router(process_router)
app.include_router(inference_router)
app.include_router(chatbot_router)

@app.get("/")
def read_root():
    return {"message": "Hello, brokie!"}