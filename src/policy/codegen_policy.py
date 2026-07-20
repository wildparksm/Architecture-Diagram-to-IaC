from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence


SAFE_EMIT_CATEGORIES = [
    "azure.networkBundle",
    "azure.virtualNetwork",
    "azure.networkSecurityGroup",
    "azure.routeTable",
    "azure.logAnalyticsWorkspace",
]

RISKY_OR_MANUAL_CATEGORIES = [
    "azure.firewall",
    "azure.avdBundle",
    "azure.avdWorkspace",
    "azure.avdHostPool",
    "azure.avdApplicationGroup",
]

KNOWN_ALLOWED_CATEGORIES = SAFE_EMIT_CATEGORIES + RISKY_OR_MANUAL_CATEGORIES


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
