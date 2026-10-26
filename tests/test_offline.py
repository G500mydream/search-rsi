import json
from pathlib import Path
import tempfile
import unittest
from dataclasses import fields

from search_rsi.agent import DemoSearchAgent
from search_rsi.environments.toy import ToyEnvironment
from search_rsi.models import ToyAnswerer
from search_rsi.runner import run
from search_rsi.types import Budget, Document, MemorySnapshot, Task

ROOT = Path(__file__).resolve().parents[1]


class OfflineTests(unittest.TestCase):
    def test_public_task_does_not_contain_labels(self):
        self.assertEqual({f.name for f in fields(Task)}, {"id", "question"})

    def test_zero_budget_performs_no_search_or_open(self):
        class ForbiddenEnvironment:
            def search(self, *args, **kwargs):
                raise AssertionError("Search called with zero budget")
            def open(self, *args, **kwargs):
                raise AssertionError("Open called with zero budget")
        agent = DemoSearchAgent(ForbiddenEnvironment(), ToyAnswerer())
        result = agent.solve(Task("x", "question"), MemorySnapshot(), Budget(0, 0))
        self.assertEqual(result.events, [])
        self.assertEqual(result.answer, "UNKNOWN")

    def test_open_budget_is_enforced(self):
        docs = [Document(str(i), "topic", "Answer: value") for i in range(3)]
        agent = DemoSearchAgent(ToyEnvironment(docs), ToyAnswerer())
        for limit in (0, 1, 2):
            with self.subTest(limit=limit):
                result = agent.solve(Task("x", "topic"), MemorySnapshot(), Budget(1, limit))
                self.assertEqual(sum(e["tool"] == "open" for e in result.events), limit)

    def test_negative_budget_rejected(self):
        with self.assertRaises(ValueError):
            Budget(-1, 1)

    def test_demo_writes_metrics_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "run"
            result = run(ROOT / "configs/demo.toml", output)
            self.assertEqual(result["tasks"], 2)
            self.assertEqual(result["exact_match"], 1.0)
            self.assertFalse(result["cross_task_learning"])
            records = [json.loads(s) for s in (output / "trajectories.jsonl").read_text().splitlines()]
            self.assertEqual(len(records), 2)
            self.assertTrue(all("gold" not in r for r in records))
            with self.assertRaises(FileExistsError):
                run(ROOT / "configs/demo.toml", output)

    def test_planned_method_fails_before_creating_output(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "run"
            with self.assertRaisesRegex(ValueError, "not implemented"):
                run(ROOT / "configs/ace.toml", output)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
