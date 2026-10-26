"""A budgeted deterministic demo agent. It is not a ReAct implementation."""
from dataclasses import asdict
from search_rsi.types import Budget, MemorySnapshot, Task, Trajectory


class DemoSearchAgent:
    def __init__(self, environment, answerer):
        self.environment = environment
        self.answerer = answerer

    def solve(self, task: Task, memory: MemorySnapshot, budget: Budget) -> Trajectory:
        events, documents = [], []
        if budget.max_search_calls:
            hits = self.environment.search(task.question)
            events.append({"tool": "search", "input": {"query": task.question},
                           "output": hits})
            for hit in hits[:budget.max_open_calls]:
                document = self.environment.open(hit["id"])
                documents.append(document)
                events.append({"tool": "open", "input": {"id": document.id},
                               "output": asdict(document)})
        answer, citations = self.answerer.answer(task.question, documents)
        return Trajectory(task.id, answer, citations, events, memory.version)
