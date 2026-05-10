# Writing Rules

Rules are small functions that receive a `ScanContext` and return findings.

```python
from rag_data_doctor.context import ScanContext
from rag_data_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    for doc in context.documents:
        if "TODO" in doc.text:
            return [finding(
                rule,
                "Document contains TODO text.",
                path=doc.path,
                recommendation="Resolve TODOs before embedding production content.",
            )]
    return []
```

Then register the rule in `src/rag_data_doctor/rules/__init__.py`:

```python
Rule(
    id="todo-text",
    title="Documents do not contain TODOs",
    category="data-quality",
    default_severity="low",
    run=todo_text,
)
```

## Context Helpers

```python
context.cwd
context.config
context.documents
context.find_documents(r"docs/.*\.md")
```

Each document has:

```python
doc.path
doc.text
doc.metadata
doc.word_count
doc.line_count
```

## Severity

- `high`: likely sensitive-data, security, privacy, or serious trust risk
- `medium`: production-readiness gap that should be fixed before embedding
- `low`: useful quality or maintainability issue
- `info`: context without a strong warning

## Good Rule Ideas

- chunk overlap detection
- missing title metadata
- source-specific freshness policies
- local link existence checks
- retrieval eval answer/source matching
- image/PDF placeholder detection
- language or encoding mismatch detection

