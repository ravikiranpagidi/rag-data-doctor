from rag_data_doctor.models import Rule
from rag_data_doctor.rules.broken_citations import run as broken_citations
from rag_data_doctor.rules.chunk_size import run as chunk_size
from rag_data_doctor.rules.duplicate_chunks import run as duplicate_chunks
from rag_data_doctor.rules.empty_documents import run as empty_documents
from rag_data_doctor.rules.metadata_completeness import run as metadata_completeness
from rag_data_doctor.rules.retrieval_eval_coverage import run as retrieval_eval_coverage
from rag_data_doctor.rules.sensitive_data import run as sensitive_data
from rag_data_doctor.rules.source_diversity import run as source_diversity
from rag_data_doctor.rules.stale_documents import run as stale_documents


RULES = [
    Rule(
        id="empty-documents",
        title="Documents contain enough text to retrieve",
        category="data-quality",
        default_severity="medium",
        run=empty_documents,
    ),
    Rule(
        id="chunk-size",
        title="Chunks are reasonably sized",
        category="retrieval-quality",
        default_severity="medium",
        run=chunk_size,
    ),
    Rule(
        id="duplicate-chunks",
        title="Duplicate or near-duplicate chunks are controlled",
        category="retrieval-quality",
        default_severity="medium",
        run=duplicate_chunks,
    ),
    Rule(
        id="metadata-completeness",
        title="Documents have source and freshness metadata",
        category="governance",
        default_severity="medium",
        run=metadata_completeness,
    ),
    Rule(
        id="stale-documents",
        title="Stale documents are visible",
        category="governance",
        default_severity="medium",
        run=stale_documents,
    ),
    Rule(
        id="broken-citations",
        title="Citations and source links are usable",
        category="trust",
        default_severity="medium",
        run=broken_citations,
    ),
    Rule(
        id="sensitive-data",
        title="Sensitive data is not embedded blindly",
        category="security",
        default_severity="high",
        run=sensitive_data,
    ),
    Rule(
        id="retrieval-eval-coverage",
        title="Retrieval eval cases are present",
        category="evaluation",
        default_severity="low",
        run=retrieval_eval_coverage,
    ),
    Rule(
        id="source-diversity",
        title="Knowledge base has enough source diversity",
        category="retrieval-quality",
        default_severity="low",
        run=source_diversity,
    ),
]

