from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.mcq import router as mcq_router
from dotenv import load_dotenv

import os

load_dotenv()

app = FastAPI(title="AI Study Assistant")

# CORS middleware (for frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Study Assistant Backend is running!", "docs": "/docs"}

app.include_router(mcq_router, prefix="/api")

