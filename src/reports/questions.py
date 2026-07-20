from __future__ import annotations

from typing import Dict, List, Tuple
from pathlib import Path
import re


def _classify_evidence_question(rec: Dict[str, object], message: str) -> tuple[str, str]:
    q_type = "Risk"
    code = "UNRESOLVED_EVIDENCE"

    if "no text label" in message.lower():
        code = "SHAPE_TEXT_MISSING"
        provenance = rec.get("provenance", {}) if isinstance(rec.get("provenance"), dict) else {}
        refs = provenance.get("evidenceRefs", []) if isinstance(provenance.get("evidenceRefs"), list) else []
        ref_name = str(refs[0]) if refs else ""

        # Generic PowerPoint auto-named shapes with no label are usually decorative frames/cards.
        if re.fullmatch(r"Shape\s+\d+", ref_name):
            q_type = "Optional"
            code = "DECORATIVE_SHAPE_UNLABELED"

    return q_type, code


def collect_questions(records: List[Dict[str, object]], graph: Dict[str, object]) -> List[Dict[str, str]]:
    questions: List[Dict[str, str]] = []

    for rec in records:
        evidence_id = str(rec.get("stableId", ""))
        for q in rec.get("unresolvedQuestions", []):
            message = str(q)
            q_type, code = _classify_evidence_question(rec, message)
            questions.append(
                {
                    "type": q_type,
                    "code": code,
                    "scope": evidence_id,
                    "message": message,
                    "lifecycle": "Detected",
                }
            )

    for q in graph.get("questions", []):
        if not isinstance(q, dict):
            continue
        questions.append(
            {
                "type": str(q.get("type", "Risk")),
                "code": str(q.get("code", "GRAPH_QUESTION")),
                "scope": str(q.get("connector", q.get("node", "graph"))),
                "message": str(q.get("message", "")),
                "lifecycle": "Detected",
            }
        )

    deduped: Dict[Tuple[str, str, str], Dict[str, str]] = {}
    for q in questions:
        key = (q["type"], q["code"], q["scope"])
        if key not in deduped:
            deduped[key] = q

    return list(deduped.values())


def write_question_report(path: Path, questions: List[Dict[str, str]]) -> None:
    blockers = [q for q in questions if q.get("type") == "Blocker"]
    risks = [q for q in questions if q.get("type") == "Risk"]
    optionals = [q for q in questions if q.get("type") == "Optional"]

    lines = [
        "# Unresolved Questions",
        "",
        "## Summary",
        f"- Total: {len(questions)}",
        f"- Blocker: {len(blockers)}",
        f"- Risk: {len(risks)}",
        f"- Optional: {len(optionals)}",
        "",
        "## Items",
    ]

    if not questions:
        lines.append("- None")
    else:
        for q in questions:
            lines.append(
                f"- [{q['type']}] ({q['code']}) scope={q['scope']} lifecycle={q['lifecycle']} :: {q['message']}"
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
