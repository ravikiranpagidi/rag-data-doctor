from __future__ import annotations

from rag_data_doctor.models import ScanResult


def print_console_report(result: ScanResult) -> None:
    counts = result.counts
    print("RAG Data Doctor")
    print(f"Path: {result.cwd}")
    print(f"Score: {result.score}/100")
    print(f"Documents scanned: {result.documents_scanned}")
    print(
        "Findings: "
        f"{counts['high']} high, {counts['medium']} medium, "
        f"{counts['low']} low, {counts['info']} info"
    )
    print()

    if not result.findings:
        print("No findings. The knowledge base looks production-aware.")
        return

    for item in result.findings:
        location = f" ({item.path})" if item.path else ""
        print(f"[{item.severity.upper()}] {item.rule_id}{location}")
        print(f"  {item.message}")
        if item.recommendation:
            print(f"  Fix: {item.recommendation}")
        print()

