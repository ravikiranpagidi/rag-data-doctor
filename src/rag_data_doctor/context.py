from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

from rag_data_doctor.models import Document


IGNORED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "venv",
}

DOCUMENT_EXTENSIONS = {
    ".md",
    ".txt",
    ".json",
    ".jsonl",
}


class ScanContext:
    def __init__(self, cwd: Path, config: dict):
        self.cwd = cwd
        self.config = config
        self.ignore_paths = tuple(config.get("ignore_paths", []))
        self.max_files = int(config.get("max_files", 3000))
        self.documents = self._load_documents()

    def find_documents(self, pattern: str) -> list[Document]:
        compiled = re.compile(pattern)
        return [doc for doc in self.documents if compiled.search(doc.path)]

    def _load_documents(self) -> list[Document]:
        docs: list[Document] = []
        roots = self._scan_roots()
        for root in roots:
            if not root.exists():
                continue
            if root.is_file():
                loaded = self._load_file(root)
                if loaded:
                    docs.append(loaded)
                continue
            for path in root.rglob("*"):
                if len(docs) >= self.max_files:
                    break
                if any(part in IGNORED_DIRECTORIES for part in path.parts):
                    continue
                relative = path.relative_to(self.cwd).as_posix()
                if self.ignore_paths and relative.startswith(self.ignore_paths):
                    continue
                if not path.is_file() or path.suffix.lower() not in DOCUMENT_EXTENSIONS:
                    continue
                loaded = self._load_file(path)
                if loaded:
                    docs.append(loaded)
        return docs

    def _scan_roots(self) -> list[Path]:
        configured = self.config.get("scan_paths") or ["."]
        return [(self.cwd / item).resolve() for item in configured]

    def _load_file(self, path: Path) -> Document | None:
        try:
            raw = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None

        relative = path.relative_to(self.cwd).as_posix()
        if path.suffix.lower() == ".json":
            return self._load_json_document(relative, path, raw)
        if path.suffix.lower() == ".jsonl":
            return self._load_jsonl_document(relative, path, raw)
        metadata, text = _split_front_matter(raw)
        return Document(path=relative, absolute_path=path, text=text, metadata=metadata)

    def _load_json_document(self, relative: str, path: Path, raw: str) -> Document:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return Document(path=relative, absolute_path=path, text=raw, metadata={})

        if isinstance(data, dict):
            text = str(data.get("text") or data.get("content") or data.get("document") or raw)
            metadata = data.get("metadata", {})
            if isinstance(metadata, dict):
                for key in ["source", "updated_at", "title", "url"]:
                    if key in data and key not in metadata:
                        metadata[key] = data[key]
            return Document(path=relative, absolute_path=path, text=text, metadata=metadata if isinstance(metadata, dict) else {})

        return Document(path=relative, absolute_path=path, text=raw, metadata={})

    def _load_jsonl_document(self, relative: str, path: Path, raw: str) -> Document:
        texts = []
        metadata = {}
        for line in raw.splitlines():
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                texts.append(line)
                continue
            if isinstance(data, dict):
                texts.append(str(data.get("text") or data.get("content") or ""))
                if isinstance(data.get("metadata"), dict):
                    metadata.update(data["metadata"])
        return Document(path=relative, absolute_path=path, text="\n".join(texts), metadata=metadata)


def _split_front_matter(raw: str) -> tuple[dict, str]:
    if not raw.startswith("---\n"):
        return {}, raw

    parts = raw.split("---\n", 2)
    if len(parts) < 3:
        return {}, raw

    metadata = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, parts[2]


def normalized_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))


def jaccard(left: Iterable[str], right: Iterable[str]) -> float:
    left_set = set(left)
    right_set = set(right)
    if not left_set and not right_set:
        return 1.0
    if not left_set or not right_set:
        return 0.0
    return len(left_set & right_set) / len(left_set | right_set)

