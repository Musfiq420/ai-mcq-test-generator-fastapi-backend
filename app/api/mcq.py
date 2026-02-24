from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import List  # ✅ Import List
import shutil
import uuid
import os

from app.services.ocr import extract_text
from app.services.chunking import chunk_text
from app.services.vector_store import add_documents, retrieve_context
from app.services.mcq_generator import generate_mcqs

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/generate-mcqs")
async def generate_mcqs_from_files(
    file: UploadFile = File(...),         # ✅ Changed to List
    num_questions: int = Form(default=10),
    difficulty: str = Form(default="medium"),
    language: str = Form(default="Bengali")      # ✅ New Input
):
    raw_text = ""

    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in [".pdf", ".png", ".jpg", ".jpeg"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    temp_filename = f"{uuid.uuid4()}{ext}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)

    # Save file
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        raw_text = extract_text(temp_path)
    finally:
        os.remove(temp_path)


    # Process the combined text
    chunks = chunk_text(raw_text)
    add_documents(chunks)

    context = retrieve_context("Important key concepts and facts for exam preparation")

    # ✅ Pass all parameters to the generator
    mcqs = generate_mcqs(
        context, 
        num_questions=num_questions, 
        difficulty=difficulty,
        language=language
    )
    
    return mcqs