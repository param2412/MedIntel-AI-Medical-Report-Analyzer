import os


def extract_text_from_image(image_path: str) -> str:
    """Extract text from a medical report image."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    return ""  # TODO: implement OCR extraction
