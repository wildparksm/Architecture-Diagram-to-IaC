from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


@dataclass
class EvidenceRecord:
    stableId: str
    source: Dict[str, str]
    kind: str
    text: str
    geometry: Dict[str, object]
    provenance: Dict[str, object]
    classificationCandidates: List[Dict[str, object]]
    confidence: Dict[str, float]
    unresolvedQuestions: List[str]
    parserVersion: str
    modelVersion: str

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


class PptxAdapter:
    parser_version = "pptx-adapter/0.1.0"

    def __init__(self, run_id: str) -> None:
        self.run_id = run_id

    def extract(self, pptx_path: Path) -> List[Dict[str, object]]:
        records: List[Dict[str, object]] = []
        document_id = pptx_path.name

        with zipfile.ZipFile(pptx_path, "r") as zf:
            slide_paths = sorted(
                [
                    name
                    for name in zf.namelist()
                    if re.match(r"^ppt/slides/slide\d+\.xml$", name)
                ],
                key=self._slide_sort_key,
            )

            for slide_path in slide_paths:
                slide_xml = zf.read(slide_path)
                root = ET.fromstring(slide_xml)
                page = Path(slide_path).name

                for sp in root.findall(".//p:sp", NS):
                    kind = self._infer_shape_kind(sp)
                    records.append(
                        self._build_record(
                            node=sp,
                            document_id=document_id,
                            page=page,
                            kind=kind,
                        )
                    )

                for cxn in root.findall(".//p:cxnSp", NS):
                    records.append(
                        self._build_record(
                            node=cxn,
                            document_id=document_id,
                            page=page,
                            kind="connector",
                        )
                    )

        return records

    def _build_record(self, node: ET.Element, document_id: str, page: str, kind: str) -> Dict[str, object]:
        nv = node.find("./p:nvSpPr/p:cNvPr", NS)
        if nv is None:
            nv = node.find("./p:nvCxnSpPr/p:cNvPr", NS)
        object_id = "unknown"
        object_name = ""
        if nv is not None:
            object_id = nv.attrib.get("id", "unknown")
            object_name = nv.attrib.get("name", "")

        text_values = [
            t.text.strip()
            for t in node.findall(".//a:t", NS)
            if t.text and t.text.strip()
        ]
        text_value = " | ".join(text_values)

        xfrm = node.find(".//a:xfrm", NS)
        geometry = self._geometry_from_xfrm(xfrm)

        stable_id = self._stable_id(document_id, page, object_id, kind)
        unresolved = []
        if not text_value and kind == "shape":
            unresolved.append("Shape has no text label. Need semantic classification confirmation.")

        evidence_refs = [object_name] if object_name else []
        if kind == "connector":
            if node.find(".//a:headEnd", NS) is not None:
                evidence_refs.append("hasHeadEnd")
            if node.find(".//a:tailEnd", NS) is not None:
                evidence_refs.append("hasTailEnd")

        record = EvidenceRecord(
            stableId=stable_id,
            source={
                "documentId": document_id,
                "page": page,
                "objectId": object_id,
            },
            kind=kind,
            text=text_value,
            geometry=geometry,
            provenance={
                "adapter": "pptx",
                "extractor": "pptx-shape-parser",
                "runId": self.run_id,
                "evidenceRefs": evidence_refs,
            },
            classificationCandidates=[
                {"label": "unknown", "score": 0.2}
            ],
            confidence={
                "existence": 1.0,
                "text": 0.95 if text_value else 0.2,
                "classification": 0.2,
                "containment": 0.5,
                "connectivity": 0.5 if kind == "connector" else 0.3,
                "deployability": 0.2,
            },
            unresolvedQuestions=unresolved,
            parserVersion=self.parser_version,
            modelVersion="none",
        )
        return record.to_dict()

    @staticmethod
    def _infer_shape_kind(node: ET.Element) -> str:
        # In this deck, many connectors are stored as p:sp with prst="line".
        prst = node.find("./p:spPr/a:prstGeom", NS)
        if prst is not None:
            preset = prst.attrib.get("prst", "").lower()
            if "line" in preset or "connector" in preset or "arrow" in preset:
                return "connector"

        nv = node.find("./p:nvSpPr/p:cNvPr", NS)
        if nv is not None:
            name = nv.attrib.get("name", "").lower()
            if "connector" in name or "line" in name or "arrow" in name:
                return "connector"

        return "shape"

    @staticmethod
    def _geometry_from_xfrm(xfrm: Optional[ET.Element]) -> Dict[str, object]:
        if xfrm is None:
            return {
                "bbox": {"x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0},
                "rotation": 0.0,
                "zOrder": 0,
            }

        off = xfrm.find("./a:off", NS)
        ext = xfrm.find("./a:ext", NS)

        def num(attr_node: Optional[ET.Element], key: str) -> float:
            if attr_node is None:
                return 0.0
            try:
                return float(attr_node.attrib.get(key, "0"))
            except ValueError:
                return 0.0

        return {
            "bbox": {
                "x": num(off, "x"),
                "y": num(off, "y"),
                "width": num(ext, "cx"),
                "height": num(ext, "cy"),
            },
            "rotation": float(xfrm.attrib.get("rot", "0")) if xfrm is not None else 0.0,
            "zOrder": 0,
        }

    @staticmethod
    def _slide_sort_key(slide_path: str) -> int:
        m = re.search(r"slide(\d+)\.xml$", slide_path)
        return int(m.group(1)) if m else 0

    @staticmethod
    def _stable_id(document_id: str, page: str, object_id: str, kind: str) -> str:
        raw = f"{document_id}:{page}:{object_id}:{kind}".encode("utf-8")
        digest = hashlib.sha1(raw).hexdigest()[:16]
        return f"ev-{digest}"


def dump_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
