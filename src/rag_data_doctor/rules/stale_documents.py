from __future__ import annotations

from datetime import date

from rag_data_doctor.context import ScanContext
from rag_data_doctor.models import Rule, finding, parse_date


def run(context: ScanContext, rule: Rule):
    max_age_days = int(context.config.get("max_document_age_days", 365))
    today = parse_date(context.config.get("today")) or date.today()
    findings = []

    for doc in context.documents:
        updated = parse_date(str(doc.metadata.get("updated_at", "")))
        if not updated:
            continue
        age = (today - updated).days
        if age > max_age_days:
            findings.append(finding(
                rule,
                f"Document is {age} days old.",
                path=doc.path,
                recommendation="Refresh stale content or mark it as archived so retrieval can down-rank it.",
            ))
            if len(findings) >= 5:
                break
    return findings

