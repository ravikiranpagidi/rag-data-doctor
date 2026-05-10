# RAG Data Doctor

RAG Data Doctor is a Python-first production-readiness scanner for RAG knowledge bases.

It helps teams answer a practical question:

> Is this knowledge base clean, fresh, citable, safe, and testable enough to power a RAG system?

The first release focuses on the problems that quietly break retrieval quality:

- duplicate or near-duplicate chunks
- chunks that are too tiny or too large
- missing `source` and `updated_at` metadata
- stale documents
- weak citation/source coverage
- sensitive data that may be embedded blindly
- missing retrieval eval cases
- low source diversity

## Quick Start

```bash
rag-data-doctor ./knowledge-base
```

From a clone:

```bash
PYTHONPATH=src python -m rag_data_doctor examples/messy-kb
PYTHONPATH=src python -m rag_data_doctor examples/healthy-kb
PYTHONPATH=src python -m rag_data_doctor --list-rules
```

This project intentionally has **zero runtime dependencies**. Python 3.10+ is enough.

## Example Output

```text
RAG Data Doctor
Path: /workspace/kb
Score: 47/100
Documents scanned: 12
Findings: 1 high, 4 medium, 1 low, 0 info

[HIGH] sensitive-data (docs/customer_notes.md)
  Possible sensitive data detected: email.
  Fix: Redact sensitive data before embedding, or document an explicit allow_sensitive_data policy.
```

## Configuration

Add `.rag-data-doctor.json` to the project you are scanning:

```json
{
  "scan_paths": ["docs"],
  "eval_paths": ["evals"],
  "min_chunk_words": 40,
  "max_chunk_words": 900,
  "max_document_age_days": 365,
  "duplicate_similarity_threshold": 0.92,
  "min_sources": 2,
  "allow_sensitive_data": false
}
```

## Metadata Format

Markdown front matter is supported:

```markdown
---
source: support-handbook
updated_at: 2026-04-01
title: Refund Policy
---

Refunds require manager approval for orders older than 30 days.
```

JSON documents are also supported:

```json
{
  "text": "Refunds require manager approval.",
  "metadata": {
    "source": "support-handbook",
    "updated_at": "2026-04-01"
  }
}
```

## Built-In Rules

| Rule | Category | Purpose |
| --- | --- | --- |
| `empty-documents` | data quality | Flags placeholder or empty documents. |
| `chunk-size` | retrieval quality | Finds chunks that are too small or too large. |
| `duplicate-chunks` | retrieval quality | Detects exact and near-duplicate content. |
| `metadata-completeness` | governance | Checks for source and freshness metadata. |
| `stale-documents` | governance | Flags old content based on `updated_at`. |
| `broken-citations` | trust | Finds documents that ask for citations but lack source links/metadata. |
| `sensitive-data` | security | Flags likely emails, API keys, tokens, or SSN-like values. |
| `retrieval-eval-coverage` | evaluation | Checks for retrieval eval cases. |
| `source-diversity` | retrieval quality | Warns when the corpus is dominated by one source. |

## Why This Exists

Many RAG projects fail because of the data layer, not the model. If the corpus is stale, duplicated, poorly chunked, missing metadata, or full of sensitive data, a better model will not fix the system.

RAG Data Doctor gives maintainers a fast first pass before documents are embedded, shipped, or used in production.

## Contributor-Friendly Roadmap

Good first issues:

- add CSV/Parquet manifest support
- add chunk overlap checks
- add broken local-file reference checks
- add query-to-source eval scoring
- add vector database export importers
- add Markdown report output
- add GitHub Action wrapper
- add language-specific token estimates
- add source freshness policies by source type

See [CONTRIBUTING.md](./CONTRIBUTING.md) and [docs/writing-rules.md](./docs/writing-rules.md).

## License

MIT

