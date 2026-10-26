"""Public task inputs are separate from evaluator-only labels."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Task:
    id: str
    question: str


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    text: str


@dataclass(frozen=True)
class Gold:
    answer: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class MemorySnapshot:
    version: int = 0
    entries: tuple[str, ...] = ()


@dataclass(frozen=True)
class Budget:
    max_search_calls: int = 1
    max_open_calls: int = 1

    def __post_init__(self):
        if self.max_search_calls < 0 or self.max_open_calls < 0:
            raise ValueError("Tool budgets must be nonnegative")


@dataclass
class Trajectory:
    task_id: str
    answer: str
    citations: list[str] = field(default_factory=list)
    events: list[dict] = field(default_factory=list)
    memory_version: int = 0
