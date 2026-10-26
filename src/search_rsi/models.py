"""Deterministic demo responder; real LLM adapters are future work."""
from search_rsi.types import Document


class ToyAnswerer:
    def answer(self, question: str, documents: list[Document]) -> tuple[str, list[str]]:
        # Deliberately simple: extract a field from retrieved synthetic documents.
        # This is a wiring check, not reasoning or evidence-grounding evaluation.
        for document in documents:
            for line in document.text.splitlines():
                if line.startswith("Answer:"):
                    return line.removeprefix("Answer:").strip(), [document.id]
        return "UNKNOWN", []
