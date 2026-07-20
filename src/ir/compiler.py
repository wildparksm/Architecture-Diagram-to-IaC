from __future__ import annotations

from typing import Dict, List, Optional
import re


def _classify_resource(name: str) -> tuple[str, str, str]:
    """Classify a resource label into (category, provider, deployability).

    provider values:
      "azure"   — emittable as Bicep/Terraform
      "onprem"  — on-premises system, document only
      "external"— external service / internet endpoint, document only
      "naver"   — Naver Cloud / Naver service, document only
      "neutral" — unknown / presentation element
    """
    lowered = name.strip().lower()
    if not lowered:
        return "unknown", "neutral", "DOCUMENTATION_ONLY"

    # ── 1. Non-Azure providers ─────────────────────────────────────────────────
    # On-premises
    _ONPREM_HINTS = [
        "nh투자", "nh securities", "ai lab", "시세", "on-prem", "on premise",
        "datacenter", "데이터센터", "legacy", "ipsec", "vpn gateway",
        "naver클라우드", "naver cloud", "naver",
    ]
    for hint in _ONPREM_HINTS:
        if hint in lowered:
            if "naver" in hint:
                return "naver.cloud", "naver", "DOCUMENTATION_ONLY"
            return "onprem.system", "onprem", "DOCUMENTATION_ONLY"

    # External / internet endpoints
    _EXTERNAL_HINTS = [
        "mts", "인터넷", "internet", "news", "외부", "external user",
        "external service", "public internet", "cdn",
    ]
    for hint in _EXTERNAL_HINTS:
        if hint in lowered:
            return "external.service", "external", "DOCUMENTATION_ONLY"

    # ── 2. Azure bundle shortcuts (multi-resource combos) ─────────────────────
    if "avd workspace / host pool / app group" in lowered:
        return "azure.avdBundle", "azure", "PARTIAL_IAC"
    if "vnet / subnet / nsg / route table" in lowered:
        return "azure.networkBundle", "azure", "PARTIAL_IAC"

    # ── 3. Separator heuristic (labels like "A | B" or "A / B" are non-resources)
    if any(token in lowered for token in ["|", "?"]):
        return "unknown", "neutral", "DOCUMENTATION_ONLY"

    # ── 4. Azure Resource Group ────────────────────────────────────────────────
    if "resource group" in lowered or re.match(r"^rg[-_]", lowered):
        return "azure.resourceGroup", "azure", "DOCUMENTATION_ONLY"

    # ── 5. Networking ─────────────────────────────────────────────────────────
    if lowered in {"vnet", "virtual network"} or " vnet" in lowered or lowered.startswith("vnet "):
        return "azure.virtualNetwork", "azure", "FULL_IAC"
    if lowered == "subnet" or lowered.startswith("subnet "):
        return "azure.subnet", "azure", "PARTIAL_IAC"
    if lowered in {"nsg", "network security group"} or " nsg" in lowered:
        return "azure.networkSecurityGroup", "azure", "FULL_IAC"
    if "route table" in lowered:
        return "azure.routeTable", "azure", "FULL_IAC"
    if "public ip" in lowered or "publicip" in lowered or "pip" == lowered:
        return "azure.publicIp", "azure", "FULL_IAC"
    if "bastion" in lowered:
        return "azure.bastionHost", "azure", "PARTIAL_IAC"
    if "ddos" in lowered:
        return "azure.ddosProtection", "azure", "PARTIAL_IAC"
    if "private dns" in lowered:
        return "azure.privateDnsZone", "azure", "PARTIAL_IAC"
    if "private endpoint" in lowered:
        return "azure.privateEndpoint", "azure", "PARTIAL_IAC"
    if "dns" in lowered and "private" not in lowered:
        return "azure.dnsResolver", "azure", "DOCUMENTATION_ONLY"

    # ── 6. Firewall / Security ────────────────────────────────────────────────
    if lowered in {"firewall", "azure firewall"} or "azure firewall" in lowered:
        return "azure.firewall", "azure", "PARTIAL_IAC"
    if "firewall policy" in lowered:
        return "azure.firewallPolicy", "azure", "PARTIAL_IAC"
    if "appgw" in lowered or "app gateway" in lowered or "application gateway" in lowered or "waf" in lowered or "appgw&waf" in lowered:
        return "azure.applicationGateway", "azure", "PARTIAL_IAC"
    if "load balancer" in lowered or "internal lb" in lowered or "ilb" == lowered:
        return "azure.loadBalancer", "azure", "PARTIAL_IAC"

    # ── 7. Compute ────────────────────────────────────────────────────────────
    if "container app" in lowered:
        return "azure.containerApp", "azure", "PARTIAL_IAC"
    if "acr" in lowered or "container registry" in lowered:
        return "azure.containerRegistry", "azure", "PARTIAL_IAC"
    if "aks" in lowered or "kubernetes" in lowered:
        return "azure.aksCluster", "azure", "PARTIAL_IAC"
    if "virtual machine" in lowered or "vm" == lowered or lowered.startswith("vm ") or " vm" in lowered:
        return "azure.virtualMachine", "azure", "PARTIAL_IAC"
    if "bastion vm" in lowered:
        return "azure.bastionHost", "azure", "PARTIAL_IAC"
    if "function app" in lowered or "azure functions" in lowered:
        return "azure.functionApp", "azure", "PARTIAL_IAC"
    if "app service" in lowered or "web app" in lowered:
        return "azure.appService", "azure", "PARTIAL_IAC"

    # ── 8. Data / Storage ─────────────────────────────────────────────────────
    if "redis" in lowered or "cache for redis" in lowered:
        return "azure.redisCache", "azure", "PARTIAL_IAC"
    if "cosmos" in lowered or "cosmosdb" in lowered:
        return "azure.cosmosDb", "azure", "PARTIAL_IAC"
    if "postgresql" in lowered or "postgres" in lowered:
        return "azure.postgresFlexible", "azure", "PARTIAL_IAC"
    if "sql database" in lowered or "azure sql" in lowered:
        return "azure.sqlDatabase", "azure", "PARTIAL_IAC"
    if "databricks" in lowered:
        return "azure.databricks", "azure", "PARTIAL_IAC"
    if "adls" in lowered or "data lake" in lowered or "adls gen2" in lowered:
        return "azure.adlsGen2", "azure", "PARTIAL_IAC"
    if "storage account" in lowered or "blob storage" in lowered or "files" == lowered:
        return "azure.storageAccount", "azure", "PARTIAL_IAC"

    # ── 9. AI / Analytics ────────────────────────────────────────────────────
    if "ai search" in lowered or "cognitive search" in lowered or "search service" in lowered:
        return "azure.cognitiveSearch", "azure", "PARTIAL_IAC"
    if "openai" in lowered or "azure openai" in lowered or "aoai" in lowered:
        return "azure.openAI", "azure", "PARTIAL_IAC"
    if "ptu" in lowered or "tpm" in lowered:
        # Azure OpenAI PTU/TPM deployment sub-resources
        return "azure.openAI", "azure", "PARTIAL_IAC"
    if "log analytics" in lowered:
        return "azure.logAnalyticsWorkspace", "azure", "FULL_IAC"
    if "diagnostic settings" in lowered or "diagnostics" in lowered:
        return "azure.diagnosticSettings", "azure", "PARTIAL_IAC"

    # ── 10. Integration / Management ─────────────────────────────────────────
    if "api management" in lowered or "apim" in lowered:
        return "azure.apiManagement", "azure", "PARTIAL_IAC"
    if "service bus" in lowered:
        return "azure.serviceBus", "azure", "PARTIAL_IAC"
    if "event hub" in lowered:
        return "azure.eventHub", "azure", "PARTIAL_IAC"
    if "key vault" in lowered or "keyvault" in lowered:
        return "azure.keyVault", "azure", "FULL_IAC"

    # ── 11. AVD ───────────────────────────────────────────────────────────────
    if lowered in {"avd workspace", "workspace"}:
        return "azure.avdWorkspace", "azure", "PARTIAL_IAC"
    if "host pool" in lowered:
        return "azure.avdHostPool", "azure", "PARTIAL_IAC"
    if "app group" in lowered:
        return "azure.avdApplicationGroup", "azure", "PARTIAL_IAC"

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
