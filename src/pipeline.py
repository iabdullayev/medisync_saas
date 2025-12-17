from src.ocr_engine import extract_text_from_pdf
from src.llm_engine import CloudLLM

class MediSyncPipeline:
    def __init__(self, api_key):
        self.llm = CloudLLM(api_key)

    def process_file(self, file_path, advocate_details=None):
        if advocate_details is None:
            advocate_details = {}

        # 1. OCR
        raw_text = extract_text_from_pdf(file_path)
        if not raw_text.strip():
            raise ValueError("OCR returned empty text. Is the PDF readable?")

        # 2. Extract Data & Draft
        # We pass the advocate_details down to the LLM now
        context = f"DENIAL LETTER CONTENT:\n{raw_text[:6000]}"
        
        draft = self.llm.draft_appeal(context, advocate_details)
        
        return {"draft": draft, "context": raw_text}