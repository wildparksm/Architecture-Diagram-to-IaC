# Deployable Resources Inventory

Source run: `run-20260715-050516`
Target scope: `resourceGroup`
Status: Draft scaffold, structurally emitted

## Actually emitted as Bicep resources

1. `Microsoft.DesktopVirtualization/hostPools@2024-04-03`
- Symbolic name: `Host_Pool`
- Display name: `Host-Pool`
- Source: standalone host pool candidate

2. `Microsoft.Network/networkSecurityGroups@2023-11-01`
- Symbolic name: `VNet_Subnet_NSG_Route_Table_nsg`
- Display name: `VNet--Subnet--NSG--Route-Table-nsg`
- Source: bundled network scaffold

3. `Microsoft.Network/routeTables@2023-11-01`
- Symbolic name: `VNet_Subnet_NSG_Route_Table_routeTable`
- Display name: `VNet--Subnet--NSG--Route-Table-rt`
- Source: bundled network scaffold

4. `Microsoft.Network/virtualNetworks@2023-11-01`
- Symbolic name: `VNet_Subnet_NSG_Route_Table_vnet`
- Display name: `VNet--Subnet--NSG--Route-Table-vnet`
- Embedded subnet: `VNet--Subnet--NSG--Route-Table-subnet`
- Source: bundled network scaffold

5. `Microsoft.DesktopVirtualization/workspaces@2024-04-03`
- Symbolic name: `AVD_Workspace_Host_Pool_App_Group_workspace`
- Display name: `AVD-Workspace--Host-Pool--App-Group-workspace`
- Source: bundled AVD scaffold

6. `Microsoft.DesktopVirtualization/hostPools@2024-04-03`
- Symbolic name: `AVD_Workspace_Host_Pool_App_Group_hostPool`
- Display name: `AVD-Workspace--Host-Pool--App-Group-hostpool`
- Source: bundled AVD scaffold

7. `Microsoft.DesktopVirtualization/applicationGroups@2024-04-03`
- Symbolic name: `AVD_Workspace_Host_Pool_App_Group_appGroup`
- Display name: `AVD-Workspace--Host-Pool--App-Group-appgroup`
- Source: bundled AVD scaffold

## Context only, not emitted as deployable resource

1. `azure.resourceGroup`
- Name: `Resource-Group`
- Reason: deployment context only under current `resourceGroup` target scope

## Deferred, not yet safe to deploy

1. `azure.firewall`
- Name: `Firewall`
- Missing: `AzureFirewallSubnet`, public IP, firewall policy/rules

2. `azure.firewall`
- Name: `Azure-Firewall`
- Missing: `AzureFirewallSubnet`, public IP, firewall policy/rules

## Notes

- The readiness gate is currently `YES`, but the generated IaC is still draft quality and needs architecture review.
- A standalone host pool and a bundled AVD host pool are both emitted, so deduplication is a good next refinement target.
