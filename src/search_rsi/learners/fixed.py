"""No cross-task learning; useful as a plumbing control."""
from search_rsi.types import MemorySnapshot


class FixedLearner:
    def snapshot(self) -> MemorySnapshot:
        return MemorySnapshot()
