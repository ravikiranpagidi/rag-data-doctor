from __future__ import annotations

from rag_data_doctor.models import Rule, finding
from rag_data_doctor.context import ScanContext


REQUIRED_FIELDS = ("source", "updated_at")


def run(context: ScanContext, rule: Rule):
    findings = []
    for doc in context.documents:
        missing = [field for field in REQUIRED_FIELDS if not doc.metadata.get(field)]
        if missing:
            findings.append(finding(
                rule,
                f"Missing metadata fields: {', '.join(missing)}.",
                path=doc.path,
                recommendation="Add source and updated_at metadata so answers can cite and age-check retrieved content.",
            ))
            if len(findings) >= 5:
                break
    return findings

