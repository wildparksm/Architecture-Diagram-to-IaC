from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import re

@dataclass
class EmittedResource:
    category: str
    symbolic_name: str
    lines: List[str]

@dataclass
class EmittedVar:
    symbolic_name: str
    lines: List[str]

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

def _expand_azure_resource(resource: Dict[str, object], idx: int) -> Tuple[List[EmittedResource], List[EmittedVar]]:
    category = str(resource.get("category", ""))
    raw_name = str(resource.get("name", ""))
    symbolic = _safe_identifier(raw_name, f"resource_{idx + 1}")
    resource_name = _safe_name(raw_name, f"resource-{idx + 1}")

    resources = []
    vars_ = []

    if category == "azure.virtualNetwork":
        resources.append(EmittedResource("azure.virtualNetwork", symbolic, [
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
        ]))
        return resources, vars_

    if category == "azure.networkSecurityGroup":
        resources.append(EmittedResource("azure.networkSecurityGroup", symbolic, [
            f"resource {symbolic} 'Microsoft.Network/networkSecurityGroups@2023-11-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  properties: {}",
            "}",
        ]))
        return resources, vars_

    if category == "azure.routeTable":
        resources.append(EmittedResource("azure.routeTable", symbolic, [
            f"resource {symbolic} 'Microsoft.Network/routeTables@2023-11-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  properties: {",
            "    disableBgpRoutePropagation: false",
            "    routes: []",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.logAnalyticsWorkspace":
        resources.append(EmittedResource("azure.logAnalyticsWorkspace", symbolic, [
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
        ]))
        return resources, vars_

    if category == "azure.keyVault":
        resources.append(EmittedResource("azure.keyVault", symbolic, [
            f"resource {symbolic} 'Microsoft.KeyVault/vaults@2023-07-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  properties: {",
            "    sku: { family: 'A', name: 'standard' }",
            "    tenantId: subscription().tenantId",
            "    enableSoftDelete: true",
            "    softDeleteRetentionInDays: 90",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.storageAccount":
        _sa_name = resource_name[:24].lower().replace("-", "")
        resources.append(EmittedResource("azure.storageAccount", symbolic, [
            f"resource {symbolic} 'Microsoft.Storage/storageAccounts@2023-05-01' = {{",
            f"  name: '{_sa_name}'",
            "  location: location",
            "  kind: 'StorageV2'",
            "  sku: { name: 'Standard_LRS' }",
            "  properties: {",
            "    minimumTlsVersion: 'TLS1_2'",
            "    allowBlobPublicAccess: false",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.adlsGen2":
        _adls_name = resource_name[:24].lower().replace("-", "")
        resources.append(EmittedResource("azure.adlsGen2", symbolic, [
            f"resource {symbolic} 'Microsoft.Storage/storageAccounts@2023-05-01' = {{",
            f"  name: '{_adls_name}'",
            "  location: location",
            "  kind: 'StorageV2'",
            "  sku: { name: 'Standard_LRS' }",
            "  properties: {",
            "    isHnsEnabled: true",
            "    minimumTlsVersion: 'TLS1_2'",
            "    allowBlobPublicAccess: false",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.loadBalancer":
        resources.append(EmittedResource("azure.loadBalancer", symbolic, [
            f"resource {symbolic} 'Microsoft.Network/loadBalancers@2023-11-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  sku: { name: 'Standard' }",
            "  properties: {",
            "    frontendIPConfigurations: []",
            "    backendAddressPools: []",
            "    loadBalancingRules: []",
            "    probes: []",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.applicationGateway":
        pip_symbolic = f"{symbolic}_pip"
        resources.append(EmittedResource("azure.publicIp", pip_symbolic, [
            f"resource {pip_symbolic} 'Microsoft.Network/publicIPAddresses@2023-11-01' = {{",
            f"  name: '{resource_name}-pip'",
            "  location: location",
            "  sku: { name: 'Standard' }",
            "  properties: { publicIPAllocationMethod: 'Static' }",
            "}",
        ]))
        resources.append(EmittedResource("azure.applicationGateway", symbolic, [
            f"resource {symbolic} 'Microsoft.Network/applicationGateways@2023-11-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  properties: {",
            "    sku: { name: 'WAF_v2', tier: 'WAF_v2', capacity: 2 }",
            "    gatewayIPConfigurations: []",
            "    frontendIPConfigurations: []",
            "    frontendPorts: []",
            "    backendAddressPools: []",
            "    backendHttpSettingsCollection: []",
            "    httpListeners: []",
            "    requestRoutingRules: []",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.bastionHost":
        pip_symbolic = f"{symbolic}_pip"
        resources.append(EmittedResource("azure.publicIp", pip_symbolic, [
            f"resource {pip_symbolic} 'Microsoft.Network/publicIPAddresses@2023-11-01' = {{",
            f"  name: '{resource_name}-pip'",
            "  location: location",
            "  sku: { name: 'Standard' }",
            "  properties: { publicIPAllocationMethod: 'Static' }",
            "}",
        ]))
        resources.append(EmittedResource("azure.bastionHost", symbolic, [
            f"resource {symbolic} 'Microsoft.Network/bastionHosts@2023-11-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  sku: { name: 'Standard' }",
            "  properties: {",
            f"    ipConfigurations: [{{ name: 'IpConf', properties: {{ publicIPAddress: {{ id: {pip_symbolic}.id }}, subnet: {{ id: 'REPLACE_WITH_SUBNET_ID' }} }} }}]",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.containerApp":
        resources.append(EmittedResource("azure.containerApp", symbolic, [
            f"resource {symbolic} 'Microsoft.App/containerApps@2024-03-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  properties: {",
            "    managedEnvironmentId: 'REPLACE_WITH_ENVIRONMENT_ID'",
            "    configuration: {",
            "      ingress: { external: false, targetPort: 80 }",
            "    }",
            "    template: {",
            "      containers: [{ name: 'app', image: 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest', resources: { cpu: json('0.5'), memory: '1Gi' } }]",
            "      scale: { minReplicas: 1, maxReplicas: 10 }",
            "    }",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.containerRegistry":
        _acr_name = resource_name.replace("-", "")
        resources.append(EmittedResource("azure.containerRegistry", symbolic, [
            f"resource {symbolic} 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' = {{",
            f"  name: '{_acr_name}'",
            "  location: location",
            "  sku: { name: 'Standard' }",
            "  properties: { adminUserEnabled: false }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.redisCache":
        resources.append(EmittedResource("azure.redisCache", symbolic, [
            f"resource {symbolic} 'Microsoft.Cache/redis@2024-03-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  properties: {",
            "    sku: { name: 'Standard', family: 'C', capacity: 1 }",
            "    enableNonSslPort: false",
            "    minimumTlsVersion: '1.2'",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.cosmosDb":
        resources.append(EmittedResource("azure.cosmosDb", symbolic, [
            f"resource {symbolic} 'Microsoft.DocumentDB/databaseAccounts@2024-05-15' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  kind: 'GlobalDocumentDB'",
            "  properties: {",
            "    consistencyPolicy: { defaultConsistencyLevel: 'Session' }",
            "    locations: [{ locationName: location, failoverPriority: 0 }]",
            "    databaseAccountOfferType: 'Standard'",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.postgresFlexible":
        resources.append(EmittedResource("azure.postgresFlexible", symbolic, [
            f"resource {symbolic} 'Microsoft.DBforPostgreSQL/flexibleServers@2024-08-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  sku: { name: 'Standard_D4s_v3', tier: 'GeneralPurpose' }",
            "  properties: {",
            "    version: '16'",
            "    storage: { storageSizeGB: 128 }",
            "    backup: { backupRetentionDays: 7, geoRedundantBackup: 'Disabled' }",
            "    administratorLogin: 'pgadmin'",
            "    administratorLoginPassword: 'REPLACE_WITH_SECURE_PASSWORD'",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.databricks":
        resources.append(EmittedResource("azure.databricks", symbolic, [
            f"resource {symbolic} 'Microsoft.Databricks/workspaces@2024-05-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  sku: { name: 'premium' }",
            "  properties: {",
            "    managedResourceGroupId: subscriptionResourceId('Microsoft.Resources/resourceGroups', '${resourceGroup().name}-databricks-managed')",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.cognitiveSearch":
        resources.append(EmittedResource("azure.cognitiveSearch", symbolic, [
            f"resource {symbolic} 'Microsoft.Search/searchServices@2024-03-01-preview' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  sku: { name: 'standard' }",
            "  properties: {",
            "    replicaCount: 1",
            "    partitionCount: 1",
            "    hostingMode: 'default'",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.openAI":
        resources.append(EmittedResource("azure.openAI", symbolic, [
            f"resource {symbolic} 'Microsoft.CognitiveServices/accounts@2024-10-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  kind: 'OpenAI'",
            "  sku: { name: 'S0' }",
            "  properties: {",
            "    customSubDomainName: '${resource_name}'",
            "    publicNetworkAccess: 'Disabled'",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.apiManagement":
        resources.append(EmittedResource("azure.apiManagement", symbolic, [
            f"resource {symbolic} 'Microsoft.ApiManagement/service@2024-05-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  sku: { name: 'Developer', capacity: 1 }",
            "  properties: {",
            "    publisherEmail: 'admin@example.com'",
            "    publisherName: 'Admin'",
            "    virtualNetworkType: 'Internal'",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.virtualMachine":
        resources.append(EmittedResource("azure.virtualMachine", symbolic, [
            f"resource {symbolic} 'Microsoft.Compute/virtualMachines@2024-07-01' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  properties: {",
            "    hardwareProfile: { vmSize: 'Standard_D4s_v5' }",
            "    storageProfile: {",
            "      imageReference: { publisher: 'MicrosoftWindowsServer', offer: 'WindowsServer', sku: '2022-datacenter-azure-edition', version: 'latest' }",
            "      osDisk: { createOption: 'FromImage', managedDisk: { storageAccountType: 'Premium_LRS' } }",
            "    }",
            "    osProfile: {",
            "      computerName: '${resource_name[:15]}'",
            "      adminUsername: 'azureadmin'",
            "      adminPassword: 'REPLACE_WITH_SECURE_PASSWORD'",
            "    }",
            "    networkProfile: { networkInterfaces: [] }",
            "  }",
            "}",
        ]))
        return resources, vars_


    if category == "azure.firewall":
        pip_symbolic = f"{symbolic}_publicIp"
        policy_symbolic = f"{symbolic}_policy"
        vnet_symbolic = f"{symbolic}_vnet"
        
        resources.append(EmittedResource("azure.publicIp", pip_symbolic, [
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
        ]))
        
        resources.append(EmittedResource("azure.firewallPolicy", policy_symbolic, [
            f"resource {policy_symbolic} 'Microsoft.Network/firewallPolicies@2023-11-01' = {{",
            f"  name: '{resource_name}-policy'",
            "  location: location",
            "  properties: {",
            "    threatIntelMode: 'Alert'",
            "  }",
            "}",
        ]))
        
        resources.append(EmittedResource("azure.virtualNetwork", vnet_symbolic, [
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
        ]))
        
        resources.append(EmittedResource("azure.firewall", symbolic, [
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
        ]))
        return resources, vars_

    if category == "azure.avdWorkspace":
        resources.append(EmittedResource("azure.avdWorkspace", symbolic, [
            f"resource {symbolic} 'Microsoft.DesktopVirtualization/workspaces@2024-04-03' = {{",
            f"  name: '{resource_name}'",
            "  location: location",
            "  properties: {",
            f"    friendlyName: '{resource_name}'",
            "    description: 'Draft workspace generated from architecture IR.'",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.avdHostPool":
        resources.append(EmittedResource("azure.avdHostPool", symbolic, [
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
        ]))
        return resources, vars_

    if category == "azure.avdBundle":
        workspace_symbolic = f"{symbolic}_workspace"
        hostpool_symbolic = f"{symbolic}_hostPool"
        appgroup_symbolic = f"{symbolic}_appGroup"
        
        resources.append(EmittedResource("azure.avdWorkspace", workspace_symbolic, [
            f"resource {workspace_symbolic} 'Microsoft.DesktopVirtualization/workspaces@2024-04-03' = {{",
            f"  name: '{resource_name}-workspace'",
            "  location: location",
            "  properties: {",
            f"    friendlyName: '{resource_name}-workspace'",
            "  }",
            "}",
        ]))
        
        resources.append(EmittedResource("azure.avdHostPool", hostpool_symbolic, [
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
        ]))
        
        resources.append(EmittedResource("azure.avdApplicationGroup", appgroup_symbolic, [
            f"resource {appgroup_symbolic} 'Microsoft.DesktopVirtualization/applicationGroups@2024-04-03' = {{",
            f"  name: '{resource_name}-appgroup'",
            "  location: location",
            "  properties: {",
            "    applicationGroupType: 'Desktop'",
            f"    hostPoolArmPath: {hostpool_symbolic}.id",
            "  }",
            "}",
        ]))
        return resources, vars_

    if category == "azure.networkBundle":
        vnet_symbolic = f"{symbolic}_vnet"
        nsg_symbolic = f"{symbolic}_nsg"
        route_symbolic = f"{symbolic}_routeTable"
        subnet_symbolic = f"{symbolic}_subnet"
        
        resources.append(EmittedResource("azure.networkSecurityGroup", nsg_symbolic, [
            f"resource {nsg_symbolic} 'Microsoft.Network/networkSecurityGroups@2023-11-01' = {{",
            f"  name: '{resource_name}-nsg'",
            "  location: location",
            "  properties: {}",
            "}",
        ]))
        
        resources.append(EmittedResource("azure.routeTable", route_symbolic, [
            f"resource {route_symbolic} 'Microsoft.Network/routeTables@2023-11-01' = {{",
            f"  name: '{resource_name}-rt'",
            "  location: location",
            "  properties: {",
            "    disableBgpRoutePropagation: false",
            "    routes: []",
            "  }",
            "}",
        ]))
        
        resources.append(EmittedResource("azure.virtualNetwork", vnet_symbolic, [
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
        ]))
        
        vars_.append(EmittedVar(subnet_symbolic, [
            f"var {subnet_symbolic} = {vnet_symbolic}.properties.subnets[0].name",
        ]))
        
        return resources, vars_

    return [], []

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

def emit_bicep(architecture_ir: Dict[str, object], output_path: Path) -> Tuple[Dict[str, str], List[str]]:
    core = architecture_ir.get("providerNeutralCore", {}) if isinstance(architecture_ir.get("providerNeutralCore"), dict) else {}
    resources = core.get("resources", []) if isinstance(core.get("resources"), list) else []
    relationships = core.get("relationships", []) if isinstance(core.get("relationships"), list) else []
    
    # We retrieve the allowed categories to perform drift analysis
    allowed_categories_list = architecture_ir.get("codegenPolicy", {}).get("allowedCategories")
    allowed_categories = set(allowed_categories_list) if allowed_categories_list is not None else None
    
    code_locations: Dict[str, str] = {}
    drift_events: List[str] = []
    
    lines: List[str] = [
        "targetScope = 'resourceGroup'",
        "",
        "@description('Draft output generated from architecture IR. Not deployment-ready without review.')",
        "param location string = resourceGroup().location",
        "",
        "@description('Safe subset of recognized Azure resources emitted as scaffold declarations.')",
    ]

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
    final_resources_to_emit: List[Tuple[List[str], List[str]]] = []

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
        
        expanded_resources, expanded_vars = _expand_azure_resource(resource, idx)
        
        if expanded_resources or expanded_vars:
            approved_resources = []
            
            for er in expanded_resources:
                if allowed_categories is not None and er.category not in allowed_categories:
                    drift_msg = f"Strict suppression: Blocked implicit resource '{er.symbolic_name}' of category '{er.category}' because it is not in the allowlist (originated from {category})."
                    drift_events.append(drift_msg)
                else:
                    approved_resources.append(er)
            
            block_lines = []
            for ar in approved_resources:
                block_lines.extend(ar.lines)
                block_lines.append("")
                
            for evar in expanded_vars:
                block_lines.extend(evar.lines)
                block_lines.append("")
                
            if block_lines:
                block_lines.pop()
                final_resources_to_emit.append((block_lines, evidence_links))
                
        else:
            if category == "azure.resourceGroup":
                contextual_resources.append(resource)
            elif category in {"azure.subnet", "azure.diagnosticSettings", "azure.avdApplicationGroup"}:
                deferred_resources.append(resource)
            else:
                unresolved_resources.append(resource)

    for block_lines, evidence_links in final_resources_to_emit:
        first_line = len(lines) + 1
        lines.extend(block_lines)
        lines.append("")
        for ev in evidence_links:
            code_locations[str(ev)] = f"main.bicep#L{first_line}"

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
    return code_locations, drift_events
