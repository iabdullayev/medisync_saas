from src.ocr_engine import extract_text_from_pdf
from src.llm_engine import CloudLLM
from src.constants import MAX_CONTEXT_LENGTH
from src.errors import OCRError, LLMError
from typing import Dict, Optional


class MediSyncPipeline:
    def __init__(self, api_key: str):
        """Initialize MediSync processing pipeline.
        
        Args:
            api_key: Groq API key for LLM
        """
        self.llm = CloudLLM(api_key)

    def process_file(self, file_path: str, advocate_details: Optional[Dict] = None) -> Dict:
        """Process a denial letter PDF and generate an appeal.
        
        Args:
            file_path: Path to the PDF file
            advocate_details: Optional dict with name, title, address
            
        Returns:
            Dictionary with 'draft' and 'context' keys
            
        Raises:
            OCRError: If OCR processing fails
            LLMError: If appeal generation fails
        """
        if advocate_details is None:
            advocate_details = {}

        # 1. OCR - Extract text from PDF
        raw_text = extract_text_from_pdf(file_path)
        if not raw_text.strip():
            raise OCRError("OCR returned empty text. Is the PDF readable?")

        # 2. Generate appeal using LLM
        # Truncate to max context length to stay within token limits
        context = f"DENIAL LETTER CONTENT:\n{raw_text[:MAX_CONTEXT_LENGTH]}"
        
        draft = self.llm.draft_appeal(context, advocate_details)
        
        return {"draft": draft, "context": raw_text}