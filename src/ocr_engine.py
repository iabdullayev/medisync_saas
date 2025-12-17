import pytesseract
from pdf2image import convert_from_path
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        # 200 DPI is faster for Cloud
        pages = convert_from_path(pdf_path, dpi=200)
        full_text = []
        for page in pages:
            text = pytesseract.image_to_string(page, config='--psm 6')
            full_text.append(text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
