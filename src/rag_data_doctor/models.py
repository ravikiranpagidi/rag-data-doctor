from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable


SEVERITY_RANK = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
}


@dataclass(frozen=True)
class Document:
    path: str
    absolute_path: Path
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def words(self) -> list[str]:
        return self.text.split()

    @property
    def word_count(self) -> int:
        return len(self.words)

    @property
    def line_count(self) -> int:
        return len(self.text.splitlines())


@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    severity: str
    category: str
    message: str
    path: str | None = None
    recommendation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "path": self.path,
            "recommendation": self.recommendation,
        }


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    category: str
    default_severity: str
    run: Callable


@dataclass
class ScanResult:
    cwd: Path
    findings: list[Finding]
    documents_scanned: int
    rules_run: int
    scanned_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def counts(self) -> dict[str, int]:
        counts = {
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0,
        }
        for finding in self.findings:
            counts[finding.severity] += 1
        return counts

    @property
    def score(self) -> int:
        penalty = 0
        for finding in self.findings:
            if finding.severity == "high":
                penalty += 20
            elif finding.severity == "medium":
                penalty += 10
            elif finding.severity == "low":
                penalty += 3
        return max(0, 100 - penalty)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool": "rag-data-doctor",
            "version": "0.1.0",
            "cwd": str(self.cwd),
            "scanned_at": self.scanned_at,
            "summary": {
                "score": self.score,
                "documents_scanned": self.documents_scanned,
                "rules_run": self.rules_run,
                "findings": len(self.findings),
                "counts": self.counts,
            },
            "findings": [finding.to_dict() for finding in self.findings],
        }


def finding(rule: Rule, message: str, *, path: str | None = None,
            severity: str | None = None, recommendation: str | None = None) -> Finding:
    return Finding(
        rule_id=rule.id,
        title=rule.title,
        severity=severity or rule.default_severity,
        category=rule.category,
        message=message,
        path=path,
        recommendation=recommendation,
    )


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None

