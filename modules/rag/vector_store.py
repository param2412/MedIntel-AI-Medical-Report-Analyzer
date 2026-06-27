from typing import Any, List


class VectorStore:
    def __init__(self):
        self.vectors: List[List[float]] = []
        self.documents: List[str] = []

    def add(self, vector: List[float], document: str) -> None:
        self.vectors.append(vector)
        self.documents.append(document)

    def search(self, query_vector: List[float], top_k: int = 5) -> List[dict[str, Any]]:
        return []  # TODO: implement similarity search
