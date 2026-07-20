# Deployable Resources Inventory

Source run: run-20260715-052644
Target scope: resourceGroup
Status: Draft scaffold, structurally emitted

## Actually emitted as Bicep resources

1. Microsoft.Network/networkSecurityGroups@2023-11-01
- Symbolic name: VNet_Subnet_NSG_Route_Table_nsg
- Name: VNet--Subnet--NSG--Route-Table-nsg

2. Microsoft.Network/routeTables@2023-11-01
- Symbolic name: VNet_Subnet_NSG_Route_Table_routeTable
- Name: VNet--Subnet--NSG--Route-Table-rt

3. Microsoft.Network/virtualNetworks@2023-11-01
- Symbolic name: VNet_Subnet_NSG_Route_Table_vnet
- Name: VNet--Subnet--NSG--Route-Table-vnet
- Embedded subnet: VNet--Subnet--NSG--Route-Table-subnet

4. Microsoft.DesktopVirtualization/workspaces@2024-04-03
- Symbolic name: AVD_Workspace_Host_Pool_App_Group_workspace
- Name: AVD-Workspace--Host-Pool--App-Group-workspace

5. Microsoft.DesktopVirtualization/hostPools@2024-04-03
- Symbolic name: AVD_Workspace_Host_Pool_App_Group_hostPool
- Name: AVD-Workspace--Host-Pool--App-Group-hostpool

6. Microsoft.DesktopVirtualization/applicationGroups@2024-04-03
- Symbolic name: AVD_Workspace_Host_Pool_App_Group_appGroup
- Name: AVD-Workspace--Host-Pool--App-Group-appgroup

## Deduplicated (not emitted)

1. Host-Pool
- Category: azure.avdHostPool
- Reason: covered-by-azure.avdBundle

## Context only, not emitted as deployable resource

1. Resource-Group
- Category: azure.resourceGroup
- Reason: deployment context only under current resourceGroup target scope

## Deferred, not yet safe to deploy

1. Firewall
- Category: azure.firewall
- Missing: AzureFirewallSubnet, public IP, firewall policy/rules

2. Azure-Firewall
- Category: azure.firewall
- Missing: AzureFirewallSubnet, public IP, firewall policy/rules
