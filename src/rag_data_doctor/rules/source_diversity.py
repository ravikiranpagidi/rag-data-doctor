from __future__ import annotations

from rag_data_doctor.context import ScanContext
from rag_data_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    if len(context.documents) < 5:
        return []

    sources = {
        str(doc.metadata.get("source") or doc.path.split("/", 1)[0])
        for doc in context.documents
    }
    min_sources = int(context.config.get("min_sources", 2))
    if len(sources) < min_sources:
        return [finding(
            rule,
            f"Only {len(sources)} source group was detected across {len(context.documents)} documents.",
            recommendation="Add source metadata and ensure the knowledge base is not dominated by a single source.",
        )]
    return []

