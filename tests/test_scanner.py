import tempfile
import unittest
from pathlib import Path

from rag_data_doctor.scanner import scan_project


class RagDataDoctorTest(unittest.TestCase):
    def test_missing_metadata_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "doc.md").write_text("This document has enough words to be useful for a retrieval system but no metadata.", encoding="utf-8")

            result = scan_project(root, only_rules=["metadata-completeness"])

        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].rule_id, "metadata-completeness")

    def test_duplicate_chunks_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text = " ".join(["refund policy requires approval"] * 10)
            (root / "one.md").write_text(text, encoding="utf-8")
            (root / "two.md").write_text(text, encoding="utf-8")

            result = scan_project(root, only_rules=["duplicate-chunks"])

        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].rule_id, "duplicate-chunks")

    def test_sensitive_data_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "doc.md").write_text("Contact customer@example.com about this private account.", encoding="utf-8")

            result = scan_project(root, only_rules=["sensitive-data"])

        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].severity, "high")

    def test_stale_document_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".rag-data-doctor.json").write_text('{"today": "2026-05-10", "max_document_age_days": 365}', encoding="utf-8")
            (root / "doc.md").write_text(
                "---\nsource: handbook\nupdated_at: 2024-01-01\n---\nThis document has policy details that are old enough to be stale.",
                encoding="utf-8",
            )

            result = scan_project(root, only_rules=["stale-documents"])

        self.assertEqual(len(result.findings), 1)
        self.assertEqual(result.findings[0].rule_id, "stale-documents")

    def test_healthy_example_has_no_high_or_medium_findings(self):
        root = Path(__file__).resolve().parents[1] / "examples" / "healthy-kb"
        result = scan_project(root)
        risky = [item for item in result.findings if item.severity in {"high", "medium"}]
        self.assertEqual(risky, [])


if __name__ == "__main__":
    unittest.main()

