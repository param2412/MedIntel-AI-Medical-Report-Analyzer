"""PDF text extraction using PyMuPDF."""

import fitz  # PyMuPDF
import os
from typing import Optional


def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extract text from a PDF file using PyMuPDF.
    
    Handles both text-based and scanned (image-based) PDFs.
    For scanned PDFs, consider using OCR via extractor.py
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text or None if extraction fails
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        Exception: If PDF is corrupted or unreadable
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    try:
        document = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(document)):
            page = document[page_num]
            text += page.get_text()
            text += "\n--- Page Break ---\n"
        
        document.close()
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_pdf_page(pdf_path: str, page_num: int) -> Optional[str]:
    """
    Extract text from a specific page in a PDF.
    
    Args:
        pdf_path: Path to the PDF file
        page_num: Page number (0-indexed)
        
    Returns:
        Extracted text from the specified page
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    try:
        document = fitz.open(pdf_path)
        
        if page_num >= len(document):
            raise ValueError(f"Page {page_num} does not exist in PDF (total pages: {len(document)})")
        
        page = document[page_num]
        text = page.get_text()
        document.close()
        
        return text
    
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF page: {str(e)}")


def get_pdf_metadata(pdf_path: str) -> dict:
    """
    Extract metadata from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary containing metadata (page count, creation date, etc.)
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    try:
        document = fitz.open(pdf_path)
        metadata = {
            "title": document.metadata.get("title", ""),
            "author": document.metadata.get("author", ""),
            "subject": document.metadata.get("subject", ""),
            "creator": document.metadata.get("creator", ""),
            "page_count": len(document),
            "is_pdf": True,
        }
        document.close()
        return metadata
    
    except Exception as e:
        raise Exception(f"Failed to extract metadata from PDF: {str(e)}")
