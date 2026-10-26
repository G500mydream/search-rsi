"""Deterministic lexical retrieval, not BM25 or a benchmark implementation."""
import re
from search_rsi.types import Document


def terms(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


class ToyEnvironment:
    def __init__(self, documents: list[Document]):
        self._documents = {d.id: d for d in documents}
        if len(self._documents) != len(documents):
            raise ValueError("Duplicate document IDs")

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if top_k < 1:
            raise ValueError("top_k must be positive")
        q = terms(query)
        scored = [(len(q & terms(d.title + " " + d.text)), d)
                  for d in self._documents.values()]
        scored.sort(key=lambda item: (-item[0], item[1].id))
        return [{"id": d.id, "title": d.title, "score": score}
                for score, d in scored[:top_k] if score > 0]

    def open(self, document_id: str) -> Document:
        return self._documents[document_id]
