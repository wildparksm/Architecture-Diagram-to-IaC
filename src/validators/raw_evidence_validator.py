from __future__ import annotations

from typing import Dict, List

REQUIRED_TOP_LEVEL = {
    "stableId",
    "source",
    "kind",
    "provenance",
    "confidence",
    "parserVersion",
}

REQUIRED_SOURCE = {"documentId", "page", "objectId"}
REQUIRED_CONFIDENCE = {
    "existence",
    "text",
    "classification",
    "containment",
    "connectivity",
    "deployability",
}


def validate_records(records: List[Dict[str, object]]) -> List[str]:
    errors: List[str] = []

    for i, record in enumerate(records):
        idx = f"record[{i}]"

        missing_top = sorted(REQUIRED_TOP_LEVEL - set(record.keys()))
        if missing_top:
            errors.append(f"{idx}: missing top-level keys: {', '.join(missing_top)}")

        source = record.get("source", {})
        if not isinstance(source, dict):
            errors.append(f"{idx}: source must be object")
        else:
            missing_source = sorted(REQUIRED_SOURCE - set(source.keys()))
            if missing_source:
                errors.append(f"{idx}: missing source keys: {', '.join(missing_source)}")

        confidence = record.get("confidence", {})
        if not isinstance(confidence, dict):
            errors.append(f"{idx}: confidence must be object")
        else:
            missing_conf = sorted(REQUIRED_CONFIDENCE - set(confidence.keys()))
            if missing_conf:
                errors.append(f"{idx}: missing confidence keys: {', '.join(missing_conf)}")
            for key in REQUIRED_CONFIDENCE:
                value = confidence.get(key)
                if not isinstance(value, (int, float)):
                    errors.append(f"{idx}: confidence.{key} must be number")
                    continue
                if value < 0 or value > 1:
                    errors.append(f"{idx}: confidence.{key} must be between 0 and 1")

    return errors
