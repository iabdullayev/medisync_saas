import pytesseract
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError
import os
from src.constants import OCR_DPI, OCR_PSM_MODE, MAX_PDF_PAGES
from src.errors import OCRError


def extract_text_from_pdf(pdf_path: str, max_pages: int = MAX_PDF_PAGES) -> str:
    """Extract text from PDF using memory-efficient streaming.
    
    This function processes PDFs page-by-page to avoid loading the entire
    document into memory, preventing OOM errors on large files.
    
    Args:
        pdf_path: Path to the PDF file
        max_pages: Maximum pages to process (prevents abuse)
        
    Returns:
        Extracted text content
        
    Raises:
        OCRError: If OCR processing fails
    """
    try:
        full_text = []
        
        # Process page by page to minimize memory usage
        for page_num in range(1, max_pages + 1):
            try:
                # Convert only one page at a time
                pages = convert_from_path(
                    pdf_path, 
                    dpi=OCR_DPI, 
                    first_page=page_num,
                    last_page=page_num
                )
                
                if not pages:
                    # No more pages
                    break
                    
                # Extract text from this page
                text = pytesseract.image_to_string(pages[0], config=OCR_PSM_MODE)
                full_text.append(text)
                
            except PDFPageCountError:
                # Reached end of document
                break
            except Exception as page_error:
                # Log page-specific error but continue processing
                print(f"Warning: Failed to process page {page_num}: {page_error}")
                continue
        
        if not full_text:
            raise OCRError("No text could be extracted from PDF")
            
        return "\n".join(full_text)
        
    except OCRError:
        # Re-raise OCRError as-is
        raise
    except Exception as e:
        raise OCRError(f"Failed to extract text from PDF: {str(e)}") from e
