from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence


# ── Tier 1: Safe — scaffold only, low blast radius ────────────────────────────
SAFE_EMIT_CATEGORIES = [
    "azure.networkBundle",
    "azure.virtualNetwork",
    "azure.networkSecurityGroup",
    "azure.routeTable",
    "azure.logAnalyticsWorkspace",
    "azure.subnet",
    "azure.publicIp",
    "azure.bastionHost",
    "azure.keyVault",
    "azure.storageAccount",
    "azure.adlsGen2",
]

# ── Tier 2: Compute / Data — need review before deploy ────────────────────────
COMPUTE_DATA_CATEGORIES = [
    "azure.containerApp",
    "azure.containerRegistry",
    "azure.aksCluster",
    "azure.loadBalancer",
    "azure.applicationGateway",
    "azure.redisCache",
    "azure.cosmosDb",
    "azure.postgresFlexible",
    "azure.sqlDatabase",
    "azure.databricks",
    "azure.cognitiveSearch",
    "azure.openAI",
    "azure.apiManagement",
    "azure.serviceBus",
    "azure.eventHub",
    "azure.functionApp",
    "azure.appService",
    "azure.virtualMachine",
    "azure.diagnosticSettings",
]

# ── Tier 3: Risky / Manual approval required ──────────────────────────────────
RISKY_OR_MANUAL_CATEGORIES = [
    "azure.firewall",
    "azure.firewallPolicy",
    "azure.avdBundle",
    "azure.avdWorkspace",
    "azure.avdHostPool",
    "azure.avdApplicationGroup",
    "azure.ddosProtection",
    "azure.privateDnsZone",
    "azure.privateEndpoint",
]

KNOWN_ALLOWED_CATEGORIES = (
    SAFE_EMIT_CATEGORIES + COMPUTE_DATA_CATEGORIES + RISKY_OR_MANUAL_CATEGORIES
)


@dataclass(frozen=True)
class CodegenPolicy:
    allowed_categories: List[str]

    @property
    def emit_none_by_default(self) -> bool:
        return len(self.allowed_categories) == 0


def normalize_allowed_categories(values: Iterable[str]) -> List[str]:
    seen = set()
    normalized: List[str] = []
    for value in values:
        candidate = value.strip()
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        normalized.append(candidate)
    return normalized


def get_known_allowed_categories() -> List[str]:
    return list(KNOWN_ALLOWED_CATEGORIES)


def find_unknown_allowed_categories(values: Sequence[str]) -> List[str]:
    normalized = normalize_allowed_categories(values)
    known = set(KNOWN_ALLOWED_CATEGORIES)
    return [value for value in normalized if value not in known]


def validate_allowed_categories(values: Sequence[str]) -> List[str]:
    normalized = normalize_allowed_categories(values)
    unknown = find_unknown_allowed_categories(normalized)
    if unknown:
        allowed = ", ".join(get_known_allowed_categories())
        invalid = ", ".join(unknown)
        raise ValueError(f"Unsupported allow categories: {invalid}. Allowed categories: {allowed}")
    return normalized
