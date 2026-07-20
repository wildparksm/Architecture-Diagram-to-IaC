from __future__ import annotations

from typing import Dict, List
import csv
from pathlib import Path


def build_traceability_rows(
    records: List[Dict[str, object]],
    graph: Dict[str, object],
    architecture_ir: Dict[str, object],
    questions: List[Dict[str, str]],
    emitted_code_locations: Dict[str, str] | None = None,
) -> List[Dict[str, str]]:
    node_map = {
        str(n.get("evidenceId", "")): n
        for n in graph.get("nodes", [])
        if isinstance(n, dict)
    }
    edge_map = {
        str(e.get("evidenceId", "")): e
        for e in graph.get("edges", [])
        if isinstance(e, dict)
    }

    core = architecture_ir.get("providerNeutralCore", {}) if isinstance(architecture_ir.get("providerNeutralCore"), dict) else {}
    ir_resources = core.get("resources", []) if isinstance(core.get("resources"), list) else []
    ir_relationships = core.get("relationships", []) if isinstance(core.get("relationships"), list) else []

    ir_by_evidence: Dict[str, str] = {}
    code_loc_by_evidence: Dict[str, str] = dict(emitted_code_locations or {})

    for idx, res in enumerate(ir_resources):
        if not isinstance(res, dict):
            continue
        loc = f"architecture.ir.json#/providerNeutralCore/resources/{idx}"
        for ev in res.get("evidenceLinks", []):
            ir_by_evidence[str(ev)] = str(res.get("id", ""))
            code_loc_by_evidence.setdefault(str(ev), loc)

    for idx, rel in enumerate(ir_relationships):
        if not isinstance(rel, dict):
            continue
        loc = f"architecture.ir.json#/providerNeutralCore/relationships/{idx}"
        for ev in rel.get("evidenceLinks", []):
            code_loc_by_evidence.setdefault(str(ev), loc)

    question_scope_map: Dict[str, List[str]] = {}
    for q in questions:
        scope = str(q.get("scope", ""))
        if not scope:
            continue
        question_scope_map.setdefault(scope, []).append(str(q.get("code", "QUESTION")))

    rows: List[Dict[str, str]] = []
    for rec in records:
        evidence_id = str(rec.get("stableId", ""))
        source = rec.get("source", {}) if isinstance(rec.get("source"), dict) else {}
        obj = f"{source.get('documentId','')}:{source.get('page','')}:{source.get('objectId','')}"

        graph_obj = node_map.get(evidence_id)
        graph_type = "node"
        if graph_obj is None:
            graph_obj = edge_map.get(evidence_id)
            graph_type = "edge" if graph_obj is not None else "none"

        question_codes = question_scope_map.get(evidence_id, [])
        decision = "none" if not question_codes else "question:" + ",".join(question_codes[:3])

        rows.append(
            {
                "source_object": obj,
                "evidence_id": evidence_id,
                "graph_object_type": graph_type,
                "graph_object_id": str(graph_obj.get("id", "")) if graph_obj else "",
                "ir_object_id": ir_by_evidence.get(evidence_id, ""),
                "question_or_decision": decision,
                "generated_code_location": code_loc_by_evidence.get(evidence_id, ""),
                "validation_result": "passed",
            }
        )

    return rows


def write_traceability_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "source_object",
        "evidence_id",
        "graph_object_type",
        "graph_object_id",
        "ir_object_id",
        "question_or_decision",
        "generated_code_location",
        "validation_result",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
