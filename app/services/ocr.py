import pytesseract
from PIL import Image
import os
import fitz




def extract_text(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_text_from_image(path)
    else:
        raise ValueError("Unsupported file type")


def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        text = page.get_text().strip()
        if text:
            pages.append(text)
    return "\n\n".join(pages)


def extract_text_from_image(image_path: str) -> str:
    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang="ben+eng")

