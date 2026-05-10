from __future__ import annotations

import re

from rag_data_doctor.context import ScanContext
from rag_data_doctor.models import Rule, finding


URL_PATTERN = re.compile(r"https?://[^\s)]+")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def run(context: ScanContext, rule: Rule):
    findings = []
    for doc in context.documents:
        urls = URL_PATTERN.findall(doc.text)
        links = MARKDOWN_LINK_PATTERN.findall(doc.text)
        if doc.metadata.get("source"):
            continue
        if urls or links:
            continue
        if "[citation needed]" in doc.text.lower() or "source:" in doc.text.lower():
            findings.append(finding(
                rule,
                "Document asks for a source or citation but no usable source metadata/link was found.",
                path=doc.path,
                recommendation="Add source metadata or a stable URL/path for citation generation.",
            ))
            break
    return findings

