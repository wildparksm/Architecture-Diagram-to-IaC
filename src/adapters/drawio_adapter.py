from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import hashlib
import xml.etree.ElementTree as ET


class DrawioAdapter:
    parser_version = "drawio-adapter/0.1.0"

    def __init__(self, run_id: str) -> None:
        self.run_id = run_id

    def extract(self, drawio_path: Path) -> List[Dict[str, object]]:
        root = ET.fromstring(drawio_path.read_text(encoding="utf-8"))
        records: List[Dict[str, object]] = []

        for cell in root.findall(".//mxCell"):
            cell_id = cell.attrib.get("id", "unknown")
            value = (cell.attrib.get("value", "") or "").strip()
            vertex = cell.attrib.get("vertex") == "1"
            edge = cell.attrib.get("edge") == "1"

            kind = "shape" if vertex else "connector" if edge else "note"
            stable_id = self._stable_id(drawio_path.name, cell_id, kind)

            records.append(
                {
                    "stableId": stable_id,
                    "source": {
                        "documentId": drawio_path.name,
                        "page": "mxGraphModel",
                        "objectId": cell_id,
                    },
                    "kind": kind,
                    "text": value,
                    "geometry": {
                        "bbox": {"x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0},
                        "rotation": 0.0,
                        "zOrder": 0,
                    },
                    "provenance": {
                        "adapter": "drawio",
                        "extractor": "drawio-xml-parser",
                        "runId": self.run_id,
                        "evidenceRefs": [],
                    },
                    "classificationCandidates": [{"label": "unknown", "score": 0.2}],
                    "confidence": {
                        "existence": 1.0,
                        "text": 0.9 if value else 0.2,
                        "classification": 0.2,
                        "containment": 0.5,
                        "connectivity": 0.5 if kind == "connector" else 0.3,
                        "deployability": 0.2,
                    },
                    "unresolvedQuestions": [],
                    "parserVersion": self.parser_version,
                    "modelVersion": "none",
                }
            )

        return records

    @staticmethod
    def _stable_id(document_id: str, object_id: str, kind: str) -> str:
        raw = f"{document_id}:{object_id}:{kind}".encode("utf-8")
        digest = hashlib.sha1(raw).hexdigest()[:16]
        return f"ev-{digest}"
