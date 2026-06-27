import os


def setup_environment() -> None:
    """Initialize environment settings and validate required directories."""
    required_dirs = [
        "data/uploaded_reports",
        "data/extracted_text",
        "data/embeddings",
    ]
    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)
