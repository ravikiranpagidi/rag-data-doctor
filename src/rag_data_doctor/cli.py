from __future__ import annotations

import argparse
import json

from rag_data_doctor.models import SEVERITY_RANK
from rag_data_doctor.reporters.console import print_console_report
from rag_data_doctor.rules import RULES
from rag_data_doctor.scanner import scan_project


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_rules:
        for rule in RULES:
            print(f"{rule.id:<28} {rule.default_severity:<7} {rule.title}")
        return 0

    result = scan_project(
        args.path,
        config_path=args.config,
        only_rules=_split_csv(args.only),
        skip_rules=_split_csv(args.skip),
    )

    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print_console_report(result)

    if args.fail_level:
        threshold = SEVERITY_RANK[args.fail_level]
        if any(SEVERITY_RANK[finding.severity] >= threshold for finding in result.findings):
            return 1

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rag-data-doctor",
        description="Scan RAG knowledge bases for data quality and production-readiness risks.",
    )
    parser.add_argument("path", nargs="?", default=".", help="Project or knowledge-base path to scan.")
    parser.add_argument("--format", choices=["console", "json"], default="console")
    parser.add_argument("--json", action="store_const", const="json", dest="format")
    parser.add_argument("--config", help="Path to JSON config file.")
    parser.add_argument("--only", help="Comma-separated rule ids to run.")
    parser.add_argument("--skip", help="Comma-separated rule ids to skip.")
    parser.add_argument("--fail-level", choices=["low", "medium", "high"])
    parser.add_argument("--list-rules", action="store_true")
    return parser


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]

