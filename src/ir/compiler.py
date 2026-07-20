from __future__ import annotations

from typing import Dict, List, Optional
import re


def _classify_resource(name: str) -> tuple[str, str, str]:
    lowered = name.strip().lower()
    if not lowered:
        return "unknown", "neutral", "DOCUMENTATION_ONLY"

    if "avd workspace / host pool / app group" in lowered:
        return "azure.avdBundle", "azure", "PARTIAL_IAC"
    if "vnet / subnet / nsg / route table" in lowered:
        return "azure.networkBundle", "azure", "PARTIAL_IAC"

    if any(token in lowered for token in ["|", "/", "?"]):
        return "unknown", "neutral", "DOCUMENTATION_ONLY"

    if "resource group" in lowered:
        return "azure.resourceGroup", "azure", "DOCUMENTATION_ONLY"
    if lowered in {"vnet", "virtual network"} or " vnet" in lowered or lowered.startswith("vnet "):
        return "azure.virtualNetwork", "azure", "FULL_IAC"
    if lowered == "subnet" or lowered.startswith("subnet "):
        return "azure.subnet", "azure", "PARTIAL_IAC"
    if lowered in {"nsg", "network security group"} or " nsg" in lowered:
        return "azure.networkSecurityGroup", "azure", "FULL_IAC"
    if "route table" in lowered:
        return "azure.routeTable", "azure", "FULL_IAC"
    if lowered in {"firewall", "azure firewall"}:
        return "azure.firewall", "azure", "PARTIAL_IAC"
    if lowered in {"avd workspace", "workspace"}:
        return "azure.avdWorkspace", "azure", "PARTIAL_IAC"
    if "host pool" in lowered:
        return "azure.avdHostPool", "azure", "PARTIAL_IAC"
    if "app group" in lowered:
        return "azure.avdApplicationGroup", "azure", "PARTIAL_IAC"
    if "log analytics" in lowered:
        return "azure.logAnalyticsWorkspace", "azure", "FULL_IAC"
    if "diagnostic settings" in lowered:
        return "azure.diagnosticSettings", "azure", "PARTIAL_IAC"

    return "unknown", "neutral", "DOCUMENTATION_ONLY"


def _should_include_unknown_resource(name: str) -> bool:
    label = name.strip()
    if not label:
        return False

    lowered = label.lower()

    if not re.search(r"[A-Za-z0-9가-힣]", label):
        return False

    if re.match(r"^\d+\s*\|", label):
        return False
    if re.match(r"^\d+\s*/\s*\|?\s*\d+", label):
        return False

    presentation_terms = [
        "architecture diagram to iac compiler",
        "problem definition",
        "key insight",
        "workflow",
        "extractor",
        "normalization",
        "question model",
        "code generation",
        "design specification",
        "validation report",
        "mvp scope",
        "roadmap",
        "vision",
        "input files",
        "multi-extractor",
        "element registry",
        "architecture review",
        "research-inspired",
        "final conclusion",
        "devops automation",
        "bicep terraform",
        "draw.io",
        "pptx",
        "shape metadata",
        "visual layout",
        "text label",
        "semantic",
        "self-ensemble",
        "confidence merge",
        "understanding engine",
        "architecture ir",
        "input files",
        "multi-stage",
        "graph reconstruction",
        "container / boundary",
        "ocr",
        "문제 정의",
        "최종 결론",
        "반복되는 수작업",
        "배포 오류 발생",
        "흩어진 아키텍처 소스",
        "의도가 코드에 미반영",
    ]
    if any(term in lowered for term in presentation_terms):
        return False

    if "?" in label or "인가" in label or "무엇인가" in label:
        return False

    if label.endswith(".") or label.endswith("다."):
        return False

    compact_alnum = re.sub(r"[^A-Za-z0-9가-힣]", "", label)
    if len(compact_alnum) <= 2:
        return False

    punctuation_count = len(re.findall(r"[-_./|·]", label))
    if punctuation_count >= max(3, len(label) // 3) and "azure" not in lowered:
        return False

    word_count = len([part for part in re.split(r"\s+", label) if part])
    has_resource_hint = any(
        token in lowered
        for token in [
            "azure",
            "vnet",
            "subnet",
            "nsg",
            "firewall",
            "host pool",
            "workspace",
            "app group",
            "route table",
            "log analytics",
            "diagnostic",
            "server",
            "gateway",
            "database",
            "storage",
            "vm",
            "network",
        ]
    )

    if lowered in {"ocr", "semantic", "shape metadata", "visual layout", "text label", "icon", "note", "input", "output"}:
        return False

    if not has_resource_hint and word_count >= 5:
        return False

    return True


def compile_ir(graph: Dict[str, object], questions: Optional[List[Dict[str, str]]] = None) -> Dict[str, object]:
    nodes = graph.get("nodes", []) if isinstance(graph.get("nodes"), list) else []
    edges = graph.get("edges", []) if isinstance(graph.get("edges"), list) else []
    effective_questions = questions if questions is not None else (
        graph.get("questions", []) if isinstance(graph.get("questions"), list) else []
    )

    resources = []
    for node in nodes:
        resource_name = str(node.get("label", ""))
        category, provider, deployability = _classify_resource(resource_name)
        if category == "unknown" and not _should_include_unknown_resource(resource_name):
            continue
        resources.append(
            {
                "id": node.get("id", ""),
                "name": resource_name,
                "category": category,
                "provider": provider,
                "deployability": deployability,
                "evidenceLinks": [node.get("evidenceId", "")],
                "confidence": node.get("confidence", {}),
            }
        )

    relationships = []
    for edge in edges:
        relationships.append(
            {
                "id": edge.get("id", ""),
                "from": edge.get("from", ""),
                "to": edge.get("to", ""),
                "kind": "dependency",
                "evidenceLinks": [edge.get("evidenceId", "")],
                "confidence": edge.get("confidence", 0.0),
            }
        )

    blocker_count = sum(
        1 for q in effective_questions if isinstance(q, dict) and str(q.get("type", "")) == "Blocker"
    )
    risk_count = sum(
        1 for q in effective_questions if isinstance(q, dict) and str(q.get("type", "")) == "Risk"
    )

    reasons = []
    if blocker_count > 0:
        reasons.append("open-blockers")
    if risk_count > 200:
        reasons.append("risk-volume-too-high")

    production_ready = len(reasons) == 0

    return {
        "version": "architecture-ir/0.1.0",
        "providerNeutralCore": {
            "resources": resources,
            "relationships": relationships,
            "containers": graph.get("zones", []),
            "securityControls": graph.get("securityControls", []),
            "existingResources": [],
            "manualControls": [],
            "assumptions": [],
            "questions": effective_questions,
            "warnings": [],
            "targetCapabilities": {
                "azureBicep": True,
                "terraformAzureRM": True,
                "multiCloud": "candidate",
                "onPremAutomation": "partial",
            },
        },
        "providerExtensions": {
            "azure": {},
            "aws": {},
            "gcp": {},
            "vmware": {},
            "kubernetes": {},
            "customUnknown": {},
        },
        "readiness": {
            "draft": True,
            "validated": False,
            "productionReady": production_ready,
            "openBlockerCount": blocker_count,
            "openRiskCount": risk_count,
            "gateReasons": reasons,
        },
    }
