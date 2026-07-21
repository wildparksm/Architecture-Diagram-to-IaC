"""image_adapter.py — Multi-provider VLM adapter for PNG/JPG architecture diagrams.

지원 프로바이더 (VLM_PROVIDER 환경변수로 선택):
  azure  → Azure OpenAI GPT-4o with Vision (기본값, 권장)
  gemini → Google Gemini Vision

환경변수 설정 (.env 파일 또는 시스템 환경변수):

  [Azure OpenAI — 권장]
  VLM_PROVIDER=azure
  AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
  AZURE_OPENAI_API_KEY=your-key
  AZURE_OPENAI_DEPLOYMENT=gpt-4o
  AZURE_OPENAI_API_VERSION=2025-01-01-preview

  [Gemini — 대안]
  VLM_PROVIDER=gemini
  GEMINI_API_KEY=your-key

사용 예:
    from src.adapters.image_adapter import ImageAdapter
    adapter = ImageAdapter(run_id="run-001")
    records = adapter.extract(Path("architecture.png"))
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


# ── Extraction Prompt ─────────────────────────────────────────────────────────
# 한국어 레이블, Azure 리소스, 온프레미스 시스템 등 모두 추출
_EXTRACTION_PROMPT = """You are an expert Azure cloud architect and infrastructure analyst.

Analyse this architecture diagram carefully and extract ALL distinct components/nodes visible.

For EACH node output a JSON object with these exact fields:
- "name": the label text shown in the diagram (preserve original text including Korean)
- "provider": one of "azure" | "onprem" | "naver" | "external" | "unknown"
- "kind": one of "resource" | "connector" | "boundary" | "label"
- "description": one brief English sentence about what this component does

Provider classification rules:
- Azure services inside Azure subscription/VNet boundaries → "azure"
- On-premises data centres, corporate networks, legacy systems, VPN endpoints → "onprem"
  (e.g. NH투자, AI LAB, 시세, on-prem data centre)
- Naver Cloud or Naver services → "naver"
- Public internet, external users, external APIs, news feeds, MTS → "external"
- Resource group boxes (rg-xxx) → kind "boundary", provider "azure"
- Arrows, lines, flow indicators → kind "connector"
- Pure text labels with no deployment meaning → kind "label"

Azure service recognition hints:
  - Firewall → azure.firewall
  - AppGW / WAF → Azure Application Gateway
  - Container Apps, ACA → Azure Container Apps
  - ACR → Azure Container Registry
  - Redis → Azure Cache for Redis
  - Databricks → Azure Databricks
  - AI Search, Cognitive Search → Azure AI Search
  - AOAI, Azure OpenAI → Azure OpenAI
  - APIM → Azure API Management
  - ADLS, Data Lake → Azure Data Lake Storage Gen2
  - PostgreSQL, Postgres → Azure Database for PostgreSQL
  - CosmosDB → Azure Cosmos DB
  - Bastion → Azure Bastion
  - Log Analytics → Azure Log Analytics Workspace
  - Key Vault, KV → Azure Key Vault

Return ONLY a valid JSON array (no markdown fences, no explanation, no trailing text):
[
  {"name": "Azure Firewall (Premium)", "provider": "azure", "kind": "resource", "description": "Azure Firewall Premium tier for traffic inspection and IDPS"},
  {"name": "NH투자", "provider": "onprem", "kind": "resource", "description": "NH Securities on-premises data centre"},
  {"name": "rg-hub-shd", "provider": "azure", "kind": "boundary", "description": "Hub shared services resource group"},
  {"name": "인터넷", "provider": "external", "kind": "resource", "description": "Public internet ingress point"}
]
"""


# ── Azure OpenAI backend ──────────────────────────────────────────────────────
def _extract_azure(image_path: Path) -> List[Dict[str, str]]:
    """Call Azure OpenAI GPT-4o Vision and parse JSON response."""
    try:
        from openai import AzureOpenAI
    except ImportError:
        raise ImportError("openai 패키지가 없습니다. 'pip install openai' 를 실행하세요.")

    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    api_key  = os.environ.get("AZURE_OPENAI_API_KEY", "")
    deploy   = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    api_ver  = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

    if not endpoint or not api_key:
        raise RuntimeError(
            "Azure OpenAI 설정이 없습니다.\n"
            ".env 파일에 다음을 설정하세요:\n"
            "  AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/\n"
            "  AZURE_OPENAI_API_KEY=your-api-key\n"
            "  AZURE_OPENAI_DEPLOYMENT=gpt-4o"
        )

    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_ver,
    )

    # Base64 인코딩
    img_bytes = image_path.read_bytes()
    suffix = image_path.suffix.lower().lstrip(".")
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    mime_type = mime_map.get(suffix, "image/png")
    b64_data = base64.b64encode(img_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model=deploy,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": _EXTRACTION_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{b64_data}",
                            "detail": "high",  # 고해상도 분석
                        },
                    },
                ],
            }
        ],
        max_tokens=4096,
        temperature=0,  # 결정적 출력 (재현 가능성)
    )

    text = response.choices[0].message.content or ""
    return _parse_vlm_response(text, provider_label="azure-openai")


# ── Gemini backend ────────────────────────────────────────────────────────────
def _extract_gemini(image_path: Path) -> List[Dict[str, str]]:
    """Call Google Gemini Vision and parse JSON response."""
    try:
        import google.generativeai as genai
    except ImportError:
        raise ImportError(
            "google-generativeai 패키지가 없습니다.\n"
            "requirements.txt 의 해당 줄 주석을 해제 후 'pip install google-generativeai' 를 실행하세요."
        )

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY 환경변수가 없습니다.\n"
            ".env 파일에 GEMINI_API_KEY=your-key 를 추가하세요."
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    img_bytes = image_path.read_bytes()
    suffix = image_path.suffix.lower().lstrip(".")
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    mime_type = mime_map.get(suffix, "image/png")

    response = model.generate_content(
        [{"mime_type": mime_type, "data": img_bytes}, _EXTRACTION_PROMPT]
    )
    return _parse_vlm_response(response.text or "", provider_label="gemini")


# ── Common JSON parser ────────────────────────────────────────────────────────
def _parse_vlm_response(text: str, provider_label: str) -> List[Dict[str, str]]:
    """Strip markdown fences and parse JSON array from VLM response."""
    text = text.strip()
    # 코드 펜스 제거
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"```\s*$", "", text, flags=re.MULTILINE).strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\[.*\]", text, re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group(0))
            except json.JSONDecodeError:
                parsed = []
        else:
            print(
                f"[image_adapter] WARNING: {provider_label} 응답이 JSON이 아닙니다.\n"
                f"  첫 500자: {text[:500]}",
                file=sys.stderr,
            )
            return []

    if not isinstance(parsed, list):
        print(
            f"[image_adapter] WARNING: {provider_label} JSON 응답이 배열이 아닙니다. type={type(parsed).__name__}",
            file=sys.stderr,
        )
        return []

    return parsed


# ── Evidence record builder ───────────────────────────────────────────────────
def _stable_id(document_id: str, name: str, idx: int) -> str:
    raw = f"{document_id}:{name}:{idx}".encode("utf-8")
    return f"ev-{hashlib.sha1(raw).hexdigest()[:16]}"


def _build_record(
    item: Dict[str, str],
    idx: int,
    document_id: str,
    run_id: str,
    vlm_provider: str,
    model_version: str,
) -> Dict[str, object]:
    name        = str(item.get("name", "")).strip()
    provider    = str(item.get("provider", "unknown")).strip()
    kind        = str(item.get("kind", "resource")).strip()
    description = str(item.get("description", "")).strip()

    stable_id = _stable_id(document_id, name, idx)
    text_conf  = 0.9 if name else 0.2
    class_conf = 0.8 if provider != "unknown" else 0.3

    unresolved = []
    if provider == "unknown":
        unresolved.append("Provider could not be determined from image. Manual classification required.")
    if kind in ("label", "connector"):
        unresolved.append("Item is a non-resource element. Verify if deployment is needed.")

    return {
        "stableId": stable_id,
        "source": {
            "documentId": document_id,
            "page": "image",
            "objectId": f"vlm-{idx}",
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
            "extractor": f"vlm/{vlm_provider}",
            "runId": run_id,
            "evidenceRefs": [description] if description else [],
            "vlmProvider": vlm_provider,
            "vlmKind": kind,
            "detectedProvider": provider,
        },
        "classificationCandidates": [
            {"label": name, "score": class_conf},
        ],
        "confidence": {
            "existence": 0.85,
            "text": text_conf,
            "classification": class_conf,
            "containment": 0.4,
            "connectivity": 0.3 if kind == "connector" else 0.2,
            "deployability": 0.7 if provider == "azure" else 0.05,
        },
        "unresolvedQuestions": unresolved,
        "parserVersion": "image-adapter/0.2.0",
        "modelVersion": model_version,
    }


# ── Public API ────────────────────────────────────────────────────────────────
class ImageAdapter:
    """Multi-provider VLM adapter.

    VLM_PROVIDER 환경변수로 백엔드를 선택합니다:
      "azure"  → Azure OpenAI GPT-4o with Vision (기본값)
      "gemini" → Google Gemini Vision

    Parameters
    ----------
    run_id : str
        파이프라인 실행 ID (provenance 필드에 주입됨)
    """

    parser_version = "image-adapter/0.2.0"

    def __init__(self, run_id: str, api_key: Optional[str] = None) -> None:
        self.run_id = run_id
        # api_key 는 Gemini 하위 호환성을 위해 남겨둠
        self._legacy_gemini_key = api_key

    @property
    def _vlm_provider(self) -> str:
        return os.environ.get("VLM_PROVIDER", "azure").lower().strip()

    def extract(self, image_path: Path) -> List[Dict[str, object]]:
        """아키텍처 이미지에서 EvidenceRecord 목록을 추출합니다."""
        provider = self._vlm_provider
        document_id = image_path.name

        if provider == "gemini":
            # 레거시 api_key 파라미터 지원
            if self._legacy_gemini_key:
                os.environ.setdefault("GEMINI_API_KEY", self._legacy_gemini_key)
            raw_items = _extract_gemini(image_path)
            model_version = "gemini-1.5-flash"
            vlm_label = "gemini"
        else:
            # 기본값: Azure OpenAI
            raw_items = _extract_azure(image_path)
            model_version = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
            vlm_label = f"azure-openai/{model_version}"

        records: List[Dict[str, object]] = []
        for idx, item in enumerate(raw_items):
            records.append(
                _build_record(
                    item=item,
                    idx=idx,
                    document_id=document_id,
                    run_id=self.run_id,
                    vlm_provider=vlm_label,
                    model_version=model_version,
                )
            )

        return records
