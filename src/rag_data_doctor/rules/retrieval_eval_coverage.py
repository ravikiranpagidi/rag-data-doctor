from __future__ import annotations

from pathlib import Path

from rag_data_doctor.context import ScanContext
from rag_data_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    eval_paths = context.config.get("eval_paths", ["evals", "tests", "retrieval_tests"])
    has_evals = any(_has_eval_file(context.cwd / path) for path in eval_paths)
    if has_evals:
        return []

    return [finding(
        rule,
        "No retrieval eval cases were found.",
        recommendation="Add a small eval set with questions, expected source ids, and expected answer facts.",
    )]


def _has_eval_file(path: Path) -> bool:
    if path.is_file():
        return path.suffix.lower() in {".json", ".jsonl"}
    if not path.exists():
        return False
    return any(
        item.is_file() and item.suffix.lower() in {".json", ".jsonl"}
        for item in path.rglob("*")
    )
