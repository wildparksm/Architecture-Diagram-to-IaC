from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import re


def _safe_identifier(value: str, fallback: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "_", value or "").strip("_")
    if not normalized:
        normalized = fallback
    if normalized[0].isdigit():
        normalized = f"r_{normalized}"
    return normalized[:64]


def _safe_name(value: str, fallback: str) -> str:
    cleaned = re.sub(r"\s+", "-", (value or "").strip())
    cleaned = re.sub(r"[^A-Za-z0-9\-_]", "", cleaned)
    return cleaned[:64] or fallback


def _emit_azure_resource(lines: List[str], resource: Dict[str, object], idx: int) -> bool:
    category = str(resource.get("category", ""))
    raw_name = str(resource.get("name", ""))
    symbolic = _safe_identifier(raw_name, f"resource_{idx + 1}")
    resource_name = _safe_name(raw_name, f"resource-{idx + 1}")

    if category == "azure.virtualNetwork":
        lines.extend(
            [
                f"resource {symbolic} 'Microsoft.Network/virtualNetworks@2023-11-01' = {{",
                f"  name: '{resource_name}'",
                "  location: location",
                "  properties: {",
                "    addressSpace: {",
                "      addressPrefixes: [",
                "        '10.0.0.0/16'",
                "      ]",
                "    }",
                "  }",
                "}",
            ]
        )
        return True

    if category == "azure.networkSecurityGroup":
        lines.extend(
            [
                f"resource {symbolic} 'Microsoft.Network/networkSecurityGroups@2023-11-01' = {{",
                f"  name: '{resource_name}'",
                "  location: location",
                "  properties: {}",
                "}",
            ]
        )
        return True

    if category == "azure.routeTable":
        lines.extend(
            [
                f"resource {symbolic} 'Microsoft.Network/routeTables@2023-11-01' = {{",
                f"  name: '{resource_name}'",
                "  location: location",
                "  properties: {",
                "    disableBgpRoutePropagation: false",
                "    routes: []",
                "  }",
                "}",
            ]
        )
        return True

    if category == "azure.logAnalyticsWorkspace":
        lines.extend(
            [
                f"resource {symbolic} 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {{",
                f"  name: '{resource_name}'",
                "  location: location",
                "  properties: {",
                "    sku: {",
                "      name: 'PerGB2018'",
                "    }",
                "    retentionInDays: 30",
                "  }",
                "}",
            ]
        )
        return True

    if category == "azure.firewall":
        pip_symbolic = f"{symbolic}_publicIp"
        policy_symbolic = f"{symbolic}_policy"
        vnet_symbolic = f"{symbolic}_vnet"
        lines.extend(
            [
                f"resource {pip_symbolic} 'Microsoft.Network/publicIPAddresses@2023-11-01' = {{",
                f"  name: '{resource_name}-pip'",
                "  location: location",
                "  sku: {",
                "    name: 'Standard'",
                "  }",
                "  properties: {",
                "    publicIPAllocationMethod: 'Static'",
                "  }",
                "}",
                "",
                f"resource {policy_symbolic} 'Microsoft.Network/firewallPolicies@2023-11-01' = {{",
                f"  name: '{resource_name}-policy'",
                "  location: location",
                "  properties: {",
                "    threatIntelMode: 'Alert'",
                "  }",
                "}",
                "",
                f"resource {vnet_symbolic} 'Microsoft.Network/virtualNetworks@2023-11-01' = {{",
                f"  name: '{resource_name}-vnet'",
                "  location: location",
                "  properties: {",
                "    addressSpace: {",
                "      addressPrefixes: [",
                "        '10.10.0.0/16'",
                "      ]",
                "    }",
                "    subnets: [",
                "      {",
                "        name: 'AzureFirewallSubnet'",
                "        properties: {",
                "          addressPrefix: '10.10.0.0/24'",
                "        }",
                "      }",
                "    ]",
                "  }",
                "}",
                "",
                f"resource {symbolic} 'Microsoft.Network/azureFirewalls@2023-11-01' = {{",
                f"  name: '{resource_name}'",
                "  location: location",
                "  properties: {",
                "    sku: {",
                "      name: 'AZFW_VNet'",
                "      tier: 'Standard'",
                "    }",
                f"    firewallPolicy: {{ id: {policy_symbolic}.id }}",
                "    ipConfigurations: [",
                "      {",
                "        name: 'azureFirewallIpConfig'",
                "        properties: {",
                f"          subnet: {{ id: {vnet_symbolic}.properties.subnets[0].id }}",
                f"          publicIPAddress: {{ id: {pip_symbolic}.id }}",
                "        }",
                "      }",
                "    ]",
                "  }",
                "}",
            ]
        )
        return True

    if category == "azure.avdWorkspace":
        lines.extend(
            [
                f"resource {symbolic} 'Microsoft.DesktopVirtualization/workspaces@2024-04-03' = {{",
                f"  name: '{resource_name}'",
                "  location: location",
                "  properties: {",
                f"    friendlyName: '{resource_name}'",
                "    description: 'Draft workspace generated from architecture IR.'",
                "  }",
                "}",
            ]
        )
        return True

    if category == "azure.avdHostPool":
        lines.extend(
            [
                f"resource {symbolic} 'Microsoft.DesktopVirtualization/hostPools@2024-04-03' = {{",
                f"  name: '{resource_name}'",
                "  location: location",
                "  properties: {",
                "    hostPoolType: 'Pooled'",
                "    loadBalancerType: 'BreadthFirst'",
                "    preferredAppGroupType: 'Desktop'",
                "    maxSessionLimit: 10",
                "    validationEnvironment: true",
                "  }",
                "}",
            ]
        )
        return True

    if category == "azure.avdBundle":
        workspace_symbolic = f"{symbolic}_workspace"
        hostpool_symbolic = f"{symbolic}_hostPool"
        appgroup_symbolic = f"{symbolic}_appGroup"
        lines.extend(
            [
                f"resource {workspace_symbolic} 'Microsoft.DesktopVirtualization/workspaces@2024-04-03' = {{",
                f"  name: '{resource_name}-workspace'",
                "  location: location",
                "  properties: {",
                f"    friendlyName: '{resource_name}-workspace'",
                "  }",
                "}",
                "",
                f"resource {hostpool_symbolic} 'Microsoft.DesktopVirtualization/hostPools@2024-04-03' = {{",
                f"  name: '{resource_name}-hostpool'",
                "  location: location",
                "  properties: {",
                "    hostPoolType: 'Pooled'",
                "    loadBalancerType: 'BreadthFirst'",
                "    preferredAppGroupType: 'Desktop'",
                "    maxSessionLimit: 10",
                "    validationEnvironment: true",
                "  }",
                "}",
                "",
                f"resource {appgroup_symbolic} 'Microsoft.DesktopVirtualization/applicationGroups@2024-04-03' = {{",
                f"  name: '{resource_name}-appgroup'",
                "  location: location",
                "  properties: {",
                "    applicationGroupType: 'Desktop'",
                f"    hostPoolArmPath: {hostpool_symbolic}.id",
                "  }",
                "}",
            ]
        )
        return True

    if category == "azure.networkBundle":
        vnet_symbolic = f"{symbolic}_vnet"
        nsg_symbolic = f"{symbolic}_nsg"
        route_symbolic = f"{symbolic}_routeTable"
        subnet_symbolic = f"{symbolic}_subnet"
        lines.extend(
            [
                f"resource {nsg_symbolic} 'Microsoft.Network/networkSecurityGroups@2023-11-01' = {{",
                f"  name: '{resource_name}-nsg'",
                "  location: location",
                "  properties: {}",
                "}",
                "",
                f"resource {route_symbolic} 'Microsoft.Network/routeTables@2023-11-01' = {{",
                f"  name: '{resource_name}-rt'",
                "  location: location",
                "  properties: {",
                "    disableBgpRoutePropagation: false",
                "    routes: []",
                "  }",
                "}",
                "",
                f"resource {vnet_symbolic} 'Microsoft.Network/virtualNetworks@2023-11-01' = {{",
                f"  name: '{resource_name}-vnet'",
                "  location: location",
                "  properties: {",
                "    addressSpace: {",
                "      addressPrefixes: [",
                "        '10.0.0.0/16'",
                "      ]",
                "    }",
                "    subnets: [",
                "      {",
                f"        name: '{resource_name}-subnet'",
                "        properties: {",
                "          addressPrefix: '10.0.0.0/24'",
                f"          networkSecurityGroup: {{ id: {nsg_symbolic}.id }}",
                f"          routeTable: {{ id: {route_symbolic}.id }}",
                "        }",
                "      }",
                "    ]",
                "  }",
                "}",
                "",
                f"var {subnet_symbolic} = {vnet_symbolic}.properties.subnets[0].name",
            ]
        )
        return True

    return False


def _emit_deferred_scaffold(lines: List[str], resource: Dict[str, object], idx: int) -> None:
    category = str(resource.get("category", ""))
    raw_name = str(resource.get("name", ""))
    symbolic = _safe_identifier(raw_name, f"deferred_{idx + 1}")
    resource_name = _safe_name(raw_name, f"deferred-{idx + 1}")

    lines.extend(
        [
            f"// Suggested scaffold for deferred resource: {raw_name or resource_name}",
            f"// category: {category or 'unknown'}",
            "// Additional provider-specific configuration is required before emission.",
            f"// resource {symbolic} '<provider/type@apiVersion>' = {{",
            f"//   name: '{resource_name}'",
            "// }}",
        ]
    )


def emit_bicep(architecture_ir: Dict[str, object], output_path: Path) -> Dict[str, str]:
    core = architecture_ir.get("providerNeutralCore", {}) if isinstance(architecture_ir.get("providerNeutralCore"), dict) else {}
    resources = core.get("resources", []) if isinstance(core.get("resources"), list) else []
    relationships = core.get("relationships", []) if isinstance(core.get("relationships"), list) else []

    lines: List[str] = [
        "targetScope = 'resourceGroup'",
        "",
        "@description('Draft output generated from architecture IR. Not deployment-ready without review.')",
        "param location string = resourceGroup().location",
        "",
        "@description('Safe subset of recognized Azure resources emitted as scaffold declarations.')",
    ]

    code_locations: Dict[str, str] = {}
    unresolved_resources: List[Dict[str, object]] = []
    contextual_resources: List[Dict[str, object]] = []
    deferred_resources: List[Dict[str, object]] = []
    deduplicated_resources: List[Dict[str, object]] = []

    has_avd_bundle = any(
        isinstance(resource, dict) and str(resource.get("category", "")) == "azure.avdBundle"
        for resource in resources
    )
    has_network_bundle = any(
        isinstance(resource, dict) and str(resource.get("category", "")) == "azure.networkBundle"
        for resource in resources
    )

    emitted_signatures = set()

    for idx, resource in enumerate(resources):
        if not isinstance(resource, dict):
            continue

        category = str(resource.get("category", ""))
        raw_name = str(resource.get("name", ""))
        resource_name = _safe_name(raw_name, f"resource-{idx + 1}")
        signature = (category, resource_name.lower())

        if has_avd_bundle and category in {"azure.avdWorkspace", "azure.avdHostPool", "azure.avdApplicationGroup"}:
            deduplicated_resources.append(
                {
                    "resource": resource,
                    "reason": "covered-by-azure.avdBundle",
                    "normalizedName": resource_name,
                }
            )
            continue

        if has_network_bundle and category in {"azure.virtualNetwork", "azure.subnet", "azure.networkSecurityGroup", "azure.routeTable"}:
            deduplicated_resources.append(
                {
                    "resource": resource,
                    "reason": "covered-by-azure.networkBundle",
                    "normalizedName": resource_name,
                }
            )
            continue

        if category.startswith("azure.") and signature in emitted_signatures:
            deduplicated_resources.append(
                {
                    "resource": resource,
                    "reason": "duplicate-category-and-name",
                    "normalizedName": resource_name,
                }
            )
            continue

        if category.startswith("azure."):
            emitted_signatures.add(signature)

        evidence_links = resource.get("evidenceLinks", []) if isinstance(resource.get("evidenceLinks"), list) else []
        first_line = len(lines) + 1
        emitted = _emit_azure_resource(lines, resource, idx)
        if emitted:
            lines.append("")
            for ev in evidence_links:
                code_locations[str(ev)] = f"main.bicep#L{first_line}"
        else:
            if category == "azure.resourceGroup":
                contextual_resources.append(resource)
            elif category in {"azure.subnet", "azure.diagnosticSettings", "azure.avdApplicationGroup"}:
                deferred_resources.append(resource)
            else:
                unresolved_resources.append(resource)

    if deduplicated_resources:
        lines.extend([
            "@description('Resources omitted from emission due to bundle-first deduplication or duplicate signatures.')",
            "var deduplicatedAzureResources = [",
        ])
        for idx, item in enumerate(deduplicated_resources):
            resource = item.get("resource", {}) if isinstance(item.get("resource"), dict) else {}
            evidence_links = resource.get("evidenceLinks", []) if isinstance(resource.get("evidenceLinks"), list) else []
            first_line = len(lines) + 1
            lines.extend(
                [
                    "  {",
                    f"    name: '{item.get('normalizedName', f'dedup-{idx + 1}')}'",
                    f"    category: '{resource.get('category', 'unknown')}'",
                    f"    reason: '{item.get('reason', 'deduplicated')}'",
                    "  }",
                ]
            )
            for ev in evidence_links:
                code_locations[str(ev)] = f"main.bicep#L{first_line}"
        lines.extend(["]", ""])

    if contextual_resources:
        lines.extend([
            "@description('Contextual Azure resources detected from source diagrams but not emitted at current target scope.')",
            "var contextualAzureResources = [",
        ])
        for idx, resource in enumerate(contextual_resources):
            evidence_links = resource.get("evidenceLinks", []) if isinstance(resource.get("evidenceLinks"), list) else []
            first_line = len(lines) + 1
            resource_name = _safe_name(str(resource.get("name", "")), f"context-{idx + 1}")
            lines.extend(
                [
                    "  {",
                    f"    name: '{resource_name}'",
                    f"    category: '{resource.get('category', 'unknown')}'",
                    "    note: 'Detected as deployment context only. Current targetScope is resourceGroup.'",
                    "  }",
                ]
            )
            for ev in evidence_links:
                code_locations[str(ev)] = f"main.bicep#L{first_line}"
        lines.extend(["]", ""])

    if deferred_resources:
        lines.extend([
            "@description('Deferred Azure scaffolds that need extra configuration before valid deployment emission.')",
            "var deferredAzureResources = [",
        ])
        for idx, resource in enumerate(deferred_resources):
            evidence_links = resource.get("evidenceLinks", []) if isinstance(resource.get("evidenceLinks"), list) else []
            first_line = len(lines) + 1
            resource_name = _safe_name(str(resource.get("name", "")), f"deferred-{idx + 1}")
            lines.extend(
                [
                    "  {",
                    f"    name: '{resource_name}'",
                    f"    category: '{resource.get('category', 'unknown')}'",
                    "    note: 'Requires additional provider-specific configuration'",
                    "  }",
                ]
            )
            for ev in evidence_links:
                code_locations[str(ev)] = f"main.bicep#L{first_line}"
        lines.extend(["]", ""])

        lines.append("// Deferred scaffold hints")
        for idx, resource in enumerate(deferred_resources):
            evidence_links = resource.get("evidenceLinks", []) if isinstance(resource.get("evidenceLinks"), list) else []
            first_line = len(lines) + 1
            _emit_deferred_scaffold(lines, resource, idx)
            lines.append("")
            for ev in evidence_links:
                code_locations[str(ev)] = f"main.bicep#L{first_line}"

    lines.extend([
        "@description('Draft architecture resources extracted from source diagrams.')",
        "var inferredResources = [",
    ])

    for idx, resource in enumerate(unresolved_resources):
        if not isinstance(resource, dict):
            continue
        evidence_links = resource.get("evidenceLinks", []) if isinstance(resource.get("evidenceLinks"), list) else []
        first_line = len(lines) + 1
        fallback_name = f"resource-{idx + 1}"
        resource_name = _safe_name(str(resource.get("name", "")), fallback_name)
        symbolic = _safe_identifier(str(resource.get("name", "")), f"resource_{idx + 1}")
        lines.extend(
            [
                "  {",
                f"    symbolicName: '{symbolic}'",
                f"    name: '{resource_name}'",
                f"    id: '{resource.get('id', '')}'",
                f"    category: '{resource.get('category', 'unknown')}'",
                f"    provider: '{resource.get('provider', 'neutral')}'",
                f"    deployability: '{resource.get('deployability', 'DOCUMENTATION_ONLY')}'",
                "  }",
            ]
        )
        for ev in evidence_links:
            code_locations[str(ev)] = f"main.bicep#L{first_line}"

    lines.extend([
        "]",
        "",
        "@description('Draft architecture relationships extracted from source diagrams.')",
        "var inferredRelationships = [",
    ])

    for relationship in relationships:
        if not isinstance(relationship, dict):
            continue
        evidence_links = relationship.get("evidenceLinks", []) if isinstance(relationship.get("evidenceLinks"), list) else []
        first_line = len(lines) + 1
        lines.extend(
            [
                "  {",
                f"    id: '{relationship.get('id', '')}'",
                f"    from: '{relationship.get('from', '')}'",
                f"    to: '{relationship.get('to', '')}'",
                f"    kind: '{relationship.get('kind', 'dependency')}'",
                "  }",
            ]
        )
        for ev in evidence_links:
            code_locations[str(ev)] = f"main.bicep#L{first_line}"

    lines.extend([
        "]",
        "",
        "output inferredResourceCount int = length(inferredResources)",
        "output inferredRelationshipCount int = length(inferredRelationships)",
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return code_locations
