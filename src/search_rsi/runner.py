"""Offline demonstration entry point. Never calls an API."""
import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tomllib

from search_rsi.agent import DemoSearchAgent
from search_rsi.environments.toy import ToyEnvironment
from search_rsi.evaluation import evaluate
from search_rsi.learners.fixed import FixedLearner
from search_rsi.logging import append_jsonl, write_json
from search_rsi.models import ToyAnswerer
from search_rsi.types import Budget, Document, Gold, Task


def run(config_path: Path, output: Path) -> dict:
    config_path = config_path.resolve()
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    if config.get("status") != "implemented" or config.get("agent") != "toy_fixed":
        raise ValueError("This configuration is planned, not implemented; use configs/demo.toml")
    fixture = (config_path.parent / config["fixture"]).resolve()
    raw = fixture.read_bytes()
    payload = json.loads(raw)
    documents = [Document(**d) for d in payload["documents"]]
    tasks = [Task(**t) for t in payload["tasks"]]
    labels = {key: Gold(value["answer"], tuple(value["evidence_ids"]))
              for key, value in payload["labels"].items()}
    if len({task.id for task in tasks}) != len(tasks):
        raise ValueError("Duplicate task IDs")
    if not tasks or any(task.id not in labels for task in tasks):
        raise ValueError("Each task must have evaluator labels")
    budget = Budget(**config["budget"])
    agent = DemoSearchAgent(ToyEnvironment(documents), ToyAnswerer())
    learner = FixedLearner()
    output.mkdir(parents=True, exist_ok=False)
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=config_path.parent,
                         capture_output=True, text=True)
    write_json(output / "manifest.json", {
        "kind": "toy_offline_demo", "started_at": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "git_commit": git.stdout.strip() if git.returncode == 0 else None,
        "fixture_sha256": hashlib.sha256(raw).hexdigest(), "config": config,
        "api_calls": 0, "note": "Synthetic plumbing check; not benchmark or learning results",
    })
    metrics = []
    for task in tasks:
        trajectory = agent.solve(task, learner.snapshot(), budget)
        # Labels are only passed to the evaluator, after the agent has returned.
        feedback = evaluate(trajectory, labels[task.id])
        append_jsonl(output / "trajectories.jsonl", asdict(trajectory))
        append_jsonl(output / "metrics.jsonl", {"task_id": task.id, **feedback})
        metrics.append(feedback)
    write_json(output / "memory.json", asdict(learner.snapshot()))
    summary = {"kind": "toy_offline_demo", "tasks": len(metrics),
               "exact_match": sum(m["exact_match"] for m in metrics) / len(metrics),
               "search_calls": sum(m["search_calls"] for m in metrics),
               "open_calls": sum(m["open_calls"] for m in metrics),
               "api_calls": 0, "cross_task_learning": False}
    write_json(output / "summary.json", summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/demo.toml"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or Path("runs") / datetime.now(timezone.utc).strftime("demo-%Y%m%dT%H%M%S%fZ")
    try:
        result = run(args.config, output)
    except (ValueError, FileExistsError) as exc:
        parser.error(str(exc))
    print(json.dumps({"output": str(output), **result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
