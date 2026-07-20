# Deployable Resources Inventory

Source run: run-20260715-073322
Target scope: resourceGroup
Status: Draft scaffold, structurally emitted

## Actually emitted as Bicep resources

1. Microsoft.Network/publicIPAddresses@2023-11-01
- Symbolic name: Firewall_publicIp
- Name: Firewall-pip

2. Microsoft.Network/firewallPolicies@2023-11-01
- Symbolic name: Firewall_policy
- Name: Firewall-policy

3. Microsoft.Network/virtualNetworks@2023-11-01
- Symbolic name: Firewall_vnet
- Name: Firewall-vnet
- Embedded subnet: AzureFirewallSubnet

4. Microsoft.Network/azureFirewalls@2023-11-01
- Symbolic name: Firewall
- Name: Firewall

5. Microsoft.Network/networkSecurityGroups@2023-11-01
- Symbolic name: VNet_Subnet_NSG_Route_Table_nsg
- Name: VNet--Subnet--NSG--Route-Table-nsg

6. Microsoft.Network/routeTables@2023-11-01
- Symbolic name: VNet_Subnet_NSG_Route_Table_routeTable
- Name: VNet--Subnet--NSG--Route-Table-rt

7. Microsoft.Network/virtualNetworks@2023-11-01
- Symbolic name: VNet_Subnet_NSG_Route_Table_vnet
- Name: VNet--Subnet--NSG--Route-Table-vnet
- Embedded subnet: VNet--Subnet--NSG--Route-Table-subnet

8. Microsoft.Network/publicIPAddresses@2023-11-01
- Symbolic name: Azure_Firewall_publicIp
- Name: Azure-Firewall-pip

9. Microsoft.Network/firewallPolicies@2023-11-01
- Symbolic name: Azure_Firewall_policy
- Name: Azure-Firewall-policy

10. Microsoft.Network/virtualNetworks@2023-11-01
- Symbolic name: Azure_Firewall_vnet
- Name: Azure-Firewall-vnet
- Embedded subnet: AzureFirewallSubnet

11. Microsoft.Network/azureFirewalls@2023-11-01
- Symbolic name: Azure_Firewall
- Name: Azure-Firewall

12. Microsoft.DesktopVirtualization/workspaces@2024-04-03
- Symbolic name: AVD_Workspace_Host_Pool_App_Group_workspace
- Name: AVD-Workspace--Host-Pool--App-Group-workspace

13. Microsoft.DesktopVirtualization/hostPools@2024-04-03
- Symbolic name: AVD_Workspace_Host_Pool_App_Group_hostPool
- Name: AVD-Workspace--Host-Pool--App-Group-hostpool

14. Microsoft.DesktopVirtualization/applicationGroups@2024-04-03
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

## Notes

- Firewall is now promoted from deferred hints to concrete scaffold resources (public IP, policy, vnet/subnet, firewall).
- There are two firewall-labeled resources in source evidence (Firewall, Azure-Firewall), so two firewall scaffold sets are emitted.
