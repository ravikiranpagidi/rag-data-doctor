from __future__ import annotations

from rag_data_doctor.context import ScanContext, jaccard, normalized_text, tokenize
from rag_data_doctor.models import Rule, finding


def run(context: ScanContext, rule: Rule):
    exact_seen: dict[str, str] = {}
    token_sets: list[tuple[str, set[str]]] = []
    threshold = float(context.config.get("duplicate_similarity_threshold", 0.92))

    for doc in context.documents:
        normalized = normalized_text(doc.text)
        if not normalized:
            continue
        if normalized in exact_seen:
            return [finding(
                rule,
                f"Exact duplicate content also appears in {exact_seen[normalized]}.",
                path=doc.path,
                recommendation="Remove duplicate chunks or keep one canonical source to avoid retrieval bias.",
            )]
        exact_seen[normalized] = doc.path

        tokens = tokenize(doc.text)
        for other_path, other_tokens in token_sets:
            if len(tokens) < 20 or len(other_tokens) < 20:
                continue
            if jaccard(tokens, other_tokens) >= threshold:
                return [finding(
                    rule,
                    f"Near-duplicate content appears similar to {other_path}.",
                    path=doc.path,
                    recommendation="Deduplicate or link related chunks so repeated text does not dominate retrieval.",
                )]
        token_sets.append((doc.path, tokens))

    return []

