"""image_adapter.py — Gemini Vision-based adapter for PNG/JPG architecture diagrams.

Sends the image to Google Gemini Vision and asks it to extract Azure and non-Azure
resources. Returns a list of EvidenceRecord-compatible dicts that plug into the
existing pipeline (IR compiler → Bicep emitter).

Environment variable required:
    GEMINI_API_KEY  — your Google AI Studio / Vertex AI API key

Usage:
    from src.adapters.image_adapter import ImageAdapter
    adapter = ImageAdapter(run_id="run-20260720-001")
    records = adapter.extract(Path("diagram.png"))
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Extraction prompt — structured so Gemini returns JSON we can parse reliably
# ---------------------------------------------------------------------------
_EXTRACTION_PROMPT = """You are an expert Azure cloud architect and infrastructure analyst.

Analyse this architecture diagram and extract ALL distinct nodes (components, services, systems) visible.

For EACH node output a JSON object with these exact fields:
- "name": the label text shown in the diagram (use original text, including Korean if present)
- "provider": one of "azure", "onprem", "naver", "external", "unknown"
- "kind": "resource" | "connector" | "boundary" | "label"
- "description": one brief sentence describing what this component does

Guidelines:
- Azure services inside Azure boundary boxes → provider "azure"
- On-premises systems, internal corporate data centres, VPN → provider "onprem"
- Naver Cloud, Naver services → provider "naver"
- Internet, external users, public endpoints, MTS, news feeds → provider "external"
- Labels, arrows, text boxes that are not components → kind "label" or "connector"
- Resource groups (rg-xxx boxes) → kind "boundary", provider "azure"
- Include ALL visible items, do not skip any

Return ONLY a JSON array like this (no markdown, no explanation):
[
  {"name": "Firewall (Primium)", "provider": "azure", "kind": "resource", "description": "Azure Firewall Premium tier for traffic inspection"},
  {"name": "NH투자", "provider": "onprem", "kind": "resource", "description": "NH Securities on-premises data centre"},
  {"name": "인터넷", "provider": "external", "kind": "resource", "description": "Public internet entry point"},
  ...
]
"""


def _gemini_extract(image_path: Path, api_key: str) -> List[Dict[str, str]]:
    """Call Gemini Vision and parse the JSON response."""
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError(
            "google-generativeai is not installed. Run: pip install google-generativeai"
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Upload image inline
    img_bytes = image_path.read_bytes()
    suffix = image_path.suffix.lower().lstrip(".")
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    mime_type = mime_map.get(suffix, "image/png")

    response = model.generate_content(
        [
            {"mime_type": mime_type, "data": img_bytes},
            _EXTRACTION_PROMPT,
        ]
    )
    text = response.text.strip()

    # Strip markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE).strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # Try to extract the first JSON array from partial output
        m = re.search(r"\[.*\]", text, re.DOTALL)
        if m:
            parsed = json.loads(m.group(0))
        else:
            raise ValueError(f"Gemini returned non-JSON output:\n{text[:500]}")

    if not isinstance(parsed, list):
        raise ValueError("Expected a JSON array from Gemini, got: " + type(parsed).__name__)

    return parsed


def _stable_id(document_id: str, name: str, idx: int) -> str:
    raw = f"{document_id}:{name}:{idx}".encode("utf-8")
    digest = hashlib.sha1(raw).hexdigest()[:16]
    return f"ev-{digest}"


def _build_record(
    item: Dict[str, str],
    idx: int,
    document_id: str,
) -> Dict[str, object]:
    name = str(item.get("name", "")).strip()
    provider = str(item.get("provider", "unknown")).strip()
    kind = str(item.get("kind", "resource")).strip()
    description = str(item.get("description", "")).strip()

    stable_id = _stable_id(document_id, name, idx)

    # Determine confidence based on what Gemini said
    text_conf = 0.9 if name else 0.2
    classification_conf = 0.7 if provider != "unknown" else 0.3

    unresolved = []
    if provider == "unknown":
        unresolved.append("Provider could not be determined from image. Manual classification required.")
    if kind in ("label", "connector"):
        unresolved.append("Item classified as non-resource element. Verify if deployment is needed.")

    return {
        "stableId": stable_id,
        "source": {
            "documentId": document_id,
            "page": "image",
            "objectId": f"gemini-{idx}",
        },
        "kind": kind,
        "text": name,
        "geometry": {
            "bbox": {"x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0},
            "rotation": 0.0,
            "zOrder": idx,
        },
        "provenance": {
            "adapter": "image",
            "extractor": "gemini-vision/1.5-flash",
            "runId": "",  # filled in by ImageAdapter
            "evidenceRefs": [description] if description else [],
            "vlmProvider": provider,
            "vlmKind": kind,
        },
        "classificationCandidates": [
            {"label": name, "score": classification_conf},
        ],
        "confidence": {
            "existence": 0.85,
            "text": text_conf,
            "classification": classification_conf,
            "containment": 0.4,
            "connectivity": 0.3 if kind == "connector" else 0.2,
            "deployability": 0.6 if provider == "azure" else 0.1,
        },
        "unresolvedQuestions": unresolved,
        "parserVersion": "image-adapter/0.1.0",
        "modelVersion": "gemini-1.5-flash",
    }


class ImageAdapter:
    """Adapter that converts a PNG/JPG architecture diagram into EvidenceRecords
    using Gemini Vision.

    Parameters
    ----------
    run_id:
        The pipeline run ID, injected into provenance fields.
    api_key:
        Gemini API key. Defaults to ``GEMINI_API_KEY`` env var.
    """

    parser_version = "image-adapter/0.1.0"

    def __init__(self, run_id: str, api_key: Optional[str] = None) -> None:
        self.run_id = run_id
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")

    def extract(self, image_path: Path) -> List[Dict[str, object]]:
        """Extract evidence records from a PNG/JPG image file.

        Returns a list of dicts compatible with the rest of the pipeline.
        """
        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set. "
                "Set it before running the image pipeline:\n"
                "  $env:GEMINI_API_KEY = 'your-api-key'"
            )

        document_id = image_path.name
        raw_items = _gemini_extract(image_path, self.api_key)

        records: List[Dict[str, object]] = []
        for idx, item in enumerate(raw_items):
            record = _build_record(item, idx, document_id)
            record["provenance"]["runId"] = self.run_id  # type: ignore[index]
            records.append(record)

        return records
