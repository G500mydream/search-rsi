"""Toy exact-match and evidence-ID checks, not a semantic citation judge."""
from search_rsi.types import Gold, Trajectory


def evaluate(trajectory: Trajectory, gold: Gold) -> dict:
    normalize = lambda s: " ".join(s.lower().split())
    retrieved = {hit["id"] for e in trajectory.events if e["tool"] == "search"
                 for hit in e["output"]}
    opened = {e["input"]["id"] for e in trajectory.events if e["tool"] == "open"}
    expected = set(gold.evidence_ids)
    cited = set(trajectory.citations)
    recall = lambda ids: len(ids & expected) / len(expected) if expected else None
    return {
        "exact_match": normalize(trajectory.answer) == normalize(gold.answer),
        "retrieved_evidence_recall": recall(retrieved),
        "opened_evidence_recall": recall(opened),
        "citation_id_precision": len(cited & expected) / len(cited) if cited else None,
        "search_calls": sum(e["tool"] == "search" for e in trajectory.events),
        "open_calls": sum(e["tool"] == "open" for e in trajectory.events),
    }
