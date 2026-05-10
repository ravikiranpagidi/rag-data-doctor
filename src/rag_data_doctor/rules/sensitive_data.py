from __future__ import annotations

import re

from rag_data_doctor.context import ScanContext
from rag_data_doctor.models import Rule, finding


PATTERNS = [
    ("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
    ("api key", re.compile(r"\b(api[_-]?key|token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}", re.IGNORECASE)),
    ("ssn-like value", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
]


def run(context: ScanContext, rule: Rule):
    allow_sensitive = bool(context.config.get("allow_sensitive_data", False))
    if allow_sensitive:
        return []

    for doc in context.documents:
        for label, pattern in PATTERNS:
            if pattern.search(doc.text):
                return [finding(
                    rule,
                    f"Possible sensitive data detected: {label}.",
                    path=doc.path,
                    recommendation="Redact sensitive data before embedding, or document an explicit allow_sensitive_data policy.",
                )]
    return []

