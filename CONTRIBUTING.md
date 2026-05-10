# Contributing to RAG Data Doctor

Thanks for helping make RAG data quality easier to check.

Useful contributions can be small:

1. Add or improve one rule in `src/rag_data_doctor/rules/`.
2. Add or update a test in `tests/`.
3. Add a short README note if behavior changed.

## Local Setup

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m rag_data_doctor examples/messy-kb
PYTHONPATH=src python -m rag_data_doctor --list-rules
```

The scanner has no runtime dependencies. Python 3.10+ is enough.

## Project Shape

```text
src/rag_data_doctor/cli.py         CLI entrypoint
src/rag_data_doctor/context.py     Document loading and text helpers
src/rag_data_doctor/scanner.py     Loads config and runs rules
src/rag_data_doctor/rules/         One file per rule
tests/                             unittest suite
examples/                          Sample knowledge bases
docs/writing-rules.md              How to add a rule
```

## Rule Guidelines

Good rules are:

- useful before embedding documents
- specific enough to avoid noisy findings
- actionable, with a clear recommendation
- testable with a tiny fixture
- relevant to retrieval quality, trust, safety, or maintainability

Avoid rules that only enforce writing style preferences.

## Pull Request Checklist

- [ ] I added or updated tests.
- [ ] I ran `PYTHONPATH=src python -m unittest discover -s tests`.
- [ ] I updated docs when needed.
- [ ] I kept the core dependency-light.

