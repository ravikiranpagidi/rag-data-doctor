from __future__ import annotations

from rag_data_doctor.context import ScanContext
from rag_data_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    min_words = int(context.config.get("min_chunk_words", 40))
    max_words = int(context.config.get("max_chunk_words", 900))
    findings = []

    for doc in context.documents:
        if doc.word_count == 0:
            continue
        if doc.word_count < min_words:
            findings.append(finding(
                rule,
                f"Chunk is very small ({doc.word_count} words).",
                path=doc.path,
                severity="low",
                recommendation="Merge tiny chunks or add surrounding context so retrieval has enough signal.",
            ))
        elif doc.word_count > max_words:
            findings.append(finding(
                rule,
                f"Chunk is very large ({doc.word_count} words).",
                path=doc.path,
                recommendation="Split large documents into smaller chunks with stable source metadata.",
            ))

        if len(findings) >= 5:
            break

    return findings

