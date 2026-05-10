from rag_data_doctor.context import ScanContext
from rag_data_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    for doc in context.documents:
        if "example" in doc.text.lower():
            return [finding(
                rule,
                "Explain the issue in plain language.",
                path=doc.path,
                recommendation="Give the maintainer one clear next step.",
            )]
    return []

