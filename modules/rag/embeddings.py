from typing import List


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Create embedding vectors for a list of texts."""
    return [[0.0] * 768 for _ in texts]  # TODO: replace with real embedding model
