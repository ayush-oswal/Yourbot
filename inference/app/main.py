from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
from app.routes.infer_route import router as infer_router

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(infer_router)

@app.get("/")
def read_root():
    return {"message": "Hello, brokie from inference!"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8001,
        reload=True
    )
