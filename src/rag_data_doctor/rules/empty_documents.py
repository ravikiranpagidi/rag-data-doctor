from __future__ import annotations

from rag_data_doctor.context import ScanContext
from rag_data_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    findings = []
    min_words = int(context.config.get("min_words", 20))
    for doc in context.documents:
        if doc.word_count < min_words:
            findings.append(finding(
                rule,
                f"Document has only {doc.word_count} words.",
                path=doc.path,
                recommendation="Remove placeholder documents or add enough content for retrieval to work.",
            ))
            if len(findings) >= 5:
                break
    return findings

