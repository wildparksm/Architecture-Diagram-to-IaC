from __future__ import annotations

from math import sqrt
from typing import Dict, List, Tuple


def _center_of(record: Dict[str, object]) -> Tuple[float, float]:
    geometry = record.get("geometry", {}) if isinstance(record, dict) else {}
    bbox = geometry.get("bbox", {}) if isinstance(geometry, dict) else {}
    x = float(bbox.get("x", 0.0))
    y = float(bbox.get("y", 0.0))
    w = float(bbox.get("width", 0.0))
    h = float(bbox.get("height", 0.0))
    return (x + w / 2.0, y + h / 2.0)


def _distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def _infer_direction(
    conn_center: Tuple[float, float],
    shape_a: Dict[str, object],
    shape_b: Dict[str, object],
) -> Tuple[Dict[str, object], Dict[str, object], str]:
    a_center = _center_of(shape_a)
    b_center = _center_of(shape_b)

    dx = abs(a_center[0] - b_center[0])
    dy = abs(a_center[1] - b_center[1])
    axis = "horizontal" if dx >= dy else "vertical"

    if axis == "horizontal":
        if a_center[0] <= b_center[0]:
            return shape_a, shape_b, "layout_left_to_right"
        return shape_b, shape_a, "layout_left_to_right"

    if a_center[1] <= b_center[1]:
        return shape_a, shape_b, "layout_top_to_bottom"
    return shape_b, shape_a, "layout_top_to_bottom"


def build_graph(records: List[Dict[str, object]]) -> Dict[str, object]:
    nodes: List[Dict[str, object]] = []
    edges: List[Dict[str, object]] = []
    questions: List[Dict[str, object]] = []

    shape_records = [r for r in records if r.get("kind") == "shape"]
    connector_records = [r for r in records if r.get("kind") == "connector"]

    for rec in shape_records:
        node_id = rec.get("stableId", "")
        source = rec.get("source", {}) if isinstance(rec.get("source"), dict) else {}
        nodes.append(
            {
                "id": node_id,
                "label": rec.get("text", ""),
                "page": source.get("page", ""),
                "objectId": source.get("objectId", ""),
                "confidence": rec.get("confidence", {}),
                "evidenceId": node_id,
            }
        )

    shapes_by_page: Dict[str, List[Dict[str, object]]] = {}
    for rec in shape_records:
        source = rec.get("source", {}) if isinstance(rec.get("source"), dict) else {}
        page = str(source.get("page", ""))
        shapes_by_page.setdefault(page, []).append(rec)

    for conn in connector_records:
        source = conn.get("source", {}) if isinstance(conn.get("source"), dict) else {}
        page = str(source.get("page", ""))
        page_shapes = shapes_by_page.get(page, [])
        if len(page_shapes) < 2:
            questions.append(
                {
                    "type": "Blocker",
                    "code": "EDGE_ENDPOINT_MISSING",
                    "connector": conn.get("stableId", ""),
                    "message": "Could not resolve connector endpoints: less than 2 shapes on page.",
                }
            )
            continue

        conn_center = _center_of(conn)
        ranked = sorted(
            [
                {
                    "record": shape,
                    "distance": _distance(conn_center, _center_of(shape)),
                }
                for shape in page_shapes
            ],
            key=lambda x: x["distance"],
        )

        chosen_a = ranked[0]
        chosen_b = ranked[1]
        from_rec, to_rec, direction_method = _infer_direction(
            conn_center,
            chosen_a["record"],
            chosen_b["record"],
        )

        total = chosen_a["distance"] + chosen_b["distance"]
        proximity_conf = 0.1 if total <= 0 else max(0.2, min(0.85, 1.0 / (1.0 + total / 1000000.0)))

        refs = conn.get("provenance", {}).get("evidenceRefs", []) if isinstance(conn.get("provenance"), dict) else []
        has_arrow_hint = "hasHeadEnd" in refs or "hasTailEnd" in refs

        ambiguity_penalty = 0.0
        if len(ranked) > 2:
            margin = ranked[2]["distance"] - ranked[1]["distance"]
            if margin < 12000:
                ambiguity_penalty = 0.15
            elif margin < 30000:
                ambiguity_penalty = 0.08

        confidence = proximity_conf + (0.08 if has_arrow_hint else 0.0) - ambiguity_penalty
        confidence = max(0.2, min(0.9, confidence))

        edges.append(
            {
                "id": conn.get("stableId", ""),
                "from": from_rec.get("stableId", ""),
                "to": to_rec.get("stableId", ""),
                "page": page,
                "evidenceId": conn.get("stableId", ""),
                "resolution": {
                    "method": "endpoint_proximity_and_layout_direction",
                    "directionMethod": direction_method,
                    "ambiguityPenalty": ambiguity_penalty,
                    "distanceA": chosen_a["distance"],
                    "distanceB": chosen_b["distance"],
                    "arrowHint": has_arrow_hint,
                },
                "confidence": confidence,
            }
        )

        if from_rec.get("stableId", "") == to_rec.get("stableId", ""):
            questions.append(
                {
                    "type": "Blocker",
                    "code": "SELF_LOOP_EDGE",
                    "connector": conn.get("stableId", ""),
                    "message": "Connector resolved to same source and target node.",
                }
            )

        if confidence < 0.5:
            questions.append(
                {
                    "type": "Risk",
                    "code": "LOW_EDGE_CONFIDENCE",
                    "connector": conn.get("stableId", ""),
                    "message": "Connector endpoint resolution has low confidence and needs review.",
                }
            )

    return {
        "version": "architecture-graph/0.1.0",
        "nodes": nodes,
        "edges": edges,
        "zones": [],
        "securityControls": [],
        "questions": questions,
    }
