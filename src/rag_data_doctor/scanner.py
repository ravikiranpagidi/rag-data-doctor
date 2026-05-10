from __future__ import annotations

import json
from pathlib import Path

from rag_data_doctor.context import ScanContext
from rag_data_doctor.models import ScanResult
from rag_data_doctor.rules import RULES


def scan_project(
    cwd: str | Path = ".",
    *,
    config_path: str | None = None,
    only_rules: list[str] | None = None,
    skip_rules: list[str] | None = None,
) -> ScanResult:
    root = Path(cwd).resolve()
    config = _load_config(root, config_path)
    selected_rules = _select_rules(
        only_rules=only_rules or config.get("only_rules", []),
        skip_rules=[*(skip_rules or []), *config.get("skip_rules", [])],
    )
    context = ScanContext(root, config)

    findings = []
    for rule in selected_rules:
        findings.extend(rule.run(context, rule))

    return ScanResult(
        cwd=root,
        findings=findings,
        documents_scanned=len(context.documents),
        rules_run=len(selected_rules),
    )


def _load_config(root: Path, config_path: str | None) -> dict:
    candidates = [root / config_path] if config_path else [
        root / ".rag-data-doctor.json",
        root / "rag-data-doctor.config.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return {}


def _select_rules(*, only_rules: list[str], skip_rules: list[str]):
    only = set(only_rules)
    skip = set(skip_rules)
    return [
        rule for rule in RULES
        if (not only or rule.id in only) and rule.id not in skip
    ]

