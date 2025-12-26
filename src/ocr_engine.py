import pytesseract
from pdf2image import convert_from_path
import os
from src.constants import OCR_DPI, OCR_PSM_MODE
from src.errors import OCRError


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF using OCR.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text content
        
    Raises:
        OCRError: If OCR processing fails
    """
    try:
        # Convert PDF to images at configured DPI
        pages = convert_from_path(pdf_path, dpi=OCR_DPI)
        full_text = []
        
        for page in pages:
            text = pytesseract.image_to_string(page, config=OCR_PSM_MODE)
            full_text.append(text)
            
        return "\n".join(full_text)
    except Exception as e:
        raise OCRError(f"Failed to extract text from PDF: {str(e)}") from e
