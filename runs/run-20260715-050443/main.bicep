targetScope = 'resourceGroup'

@description('Draft output generated from architecture IR. Not deployment-ready without review.')
param location string = resourceGroup().location

@description('Safe subset of recognized Azure resources emitted as scaffold declarations.')
resource Host_Pool 'Microsoft.DesktopVirtualization/hostPools@2024-04-03' = {
  name: 'Host-Pool'
  location: location
  properties: {
    hostPoolType: 'Pooled'
    loadBalancerType: 'BreadthFirst'
    preferredAppGroupType: 'Desktop'
    maxSessionLimit: 10
    validationEnvironment: true
  }
}

resource VNet_Subnet_NSG_Route_Table_nsg 'Microsoft.Network/networkSecurityGroups@2023-11-01' = {
  name: 'VNet--Subnet--NSG--Route-Table-nsg'
  location: location
  properties: {}
}

resource VNet_Subnet_NSG_Route_Table_routeTable 'Microsoft.Network/routeTables@2023-11-01' = {
  name: 'VNet--Subnet--NSG--Route-Table-rt'
  location: location
  properties: {
    disableBgpRoutePropagation: false
    routes: []
  }
}

resource VNet_Subnet_NSG_Route_Table_vnet 'Microsoft.Network/virtualNetworks@2023-11-01' = {
  name: 'VNet--Subnet--NSG--Route-Table-vnet'
  location: location
  properties: {
    addressSpace: {
      addressPrefixes: [
        '10.0.0.0/16'
      ]
    }
    subnets: [
      {
        name: 'VNet--Subnet--NSG--Route-Table-subnet'
        properties: {
          addressPrefix: '10.0.0.0/24'
          networkSecurityGroup: { id: VNet_Subnet_NSG_Route_Table_nsg.id }
          routeTable: { id: VNet_Subnet_NSG_Route_Table_routeTable.id }
        }
      }
    ]
  }
}

var VNet_Subnet_NSG_Route_Table_subnet = VNet_Subnet_NSG_Route_Table_vnet.properties.subnets[0].name

resource AVD_Workspace_Host_Pool_App_Group_workspace 'Microsoft.DesktopVirtualization/workspaces@2024-04-03' = {
  name: 'AVD-Workspace--Host-Pool--App-Group-workspace'
  location: location
  properties: {
    friendlyName: 'AVD-Workspace--Host-Pool--App-Group-workspace'
  }
}

resource AVD_Workspace_Host_Pool_App_Group_hostPool 'Microsoft.DesktopVirtualization/hostPools@2024-04-03' = {
  name: 'AVD-Workspace--Host-Pool--App-Group-hostpool'
  location: location
  properties: {
    hostPoolType: 'Pooled'
    loadBalancerType: 'BreadthFirst'
    preferredAppGroupType: 'Desktop'
    maxSessionLimit: 10
    validationEnvironment: true
  }
}

resource AVD_Workspace_Host_Pool_App_Group_appGroup 'Microsoft.DesktopVirtualization/applicationGroups@2024-04-03' = {
  name: 'AVD-Workspace--Host-Pool--App-Group-appgroup'
  location: location
  properties: {
    applicationGroupType: 'Desktop'
    hostPoolArmPath: AVD_Workspace_Host_Pool_App_Group_hostPool.id
  }
}

@description('Contextual Azure resources detected from source diagrams but not emitted at current target scope.')
var contextualAzureResources = [
  {
    name: 'Resource-Group'
    category: 'azure.resourceGroup'
    note: 'Detected as deployment context only. Current targetScope is resourceGroup.'
  }
]

@description('Deferred Azure scaffolds that need extra configuration before valid deployment emission.')
var deferredAzureResources = [
  {
    name: 'Firewall'
    category: 'azure.firewall'
    note: 'Requires AzureFirewallSubnet, public IPs, and policy/rule configuration'
  }
  {
    name: 'Azure-Firewall'
    category: 'azure.firewall'
    note: 'Requires AzureFirewallSubnet, public IPs, and policy/rule configuration'
  }
]

// Deferred scaffold hints
// Suggested scaffold for deferred resource: Firewall
// resource Firewall 'Microsoft.Network/azureFirewalls@2023-11-01' = {
//   name: 'Firewall'
//   location: location
//   properties: {
//     sku: {
//       name: 'AZFW_VNet'
//       tier: 'Standard'
//     }
//     ipConfigurations: [
//       {
//         name: 'azureFirewallIpConfig'
//         properties: {
//           subnet: {
//             id: '<AzureFirewallSubnet-resource-id>'
//           }
//           publicIPAddress: {
//             id: '<public-ip-resource-id>'
//           }
//         }
//       }
//     ]
//   }
// }

// Suggested scaffold for deferred resource: Azure Firewall
// resource Azure_Firewall 'Microsoft.Network/azureFirewalls@2023-11-01' = {
//   name: 'Azure-Firewall'
//   location: location
//   properties: {
//     sku: {
//       name: 'AZFW_VNet'
//       tier: 'Standard'
//     }
//     ipConfigurations: [
//       {
//         name: 'azureFirewallIpConfig'
//         properties: {
//           subnet: {
//             id: '<AzureFirewallSubnet-resource-id>'
//           }
//           publicIPAddress: {
//             id: '<public-ip-resource-id>'
//           }
//         }
//       }
//     ]
//   }
// }

@description('Draft architecture resources extracted from source diagrams.')
var inferredResources = [
  {
    symbolicName: 'Azure_Bicep_Terraform'
    name: '---Azure-BicepTerraform----'
    id: 'ev-d75715e51f99c0a2'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_2'
    name: '--'
    id: 'ev-92c04b84fb3bb8b3'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_3'
    name: '-'
    id: 'ev-4695597240ee5ba1'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'text_label'
    name: 'text--label'
    id: 'ev-b2158c5943c148b1'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_5'
    name: '-'
    id: 'ev-b3c2cf21a8d93962'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Azure_resource'
    name: 'Azure-resource'
    id: 'ev-119cf002bb775092'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'LLM_Reasoning'
    name: 'LLM-Reasoning'
    id: 'ev-6b2d425c8eb1e9b1'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_1'
    name: '1'
    id: 'ev-8d88d8a5cbea7778'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_2'
    name: '2'
    id: 'ev-5fc729aa7775f648'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_3'
    name: '3'
    id: 'ev-9b9c59e7d5f40a9c'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_4'
    name: '4'
    id: 'ev-43d26d357ccb054b'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_5'
    name: '5'
    id: 'ev-89d21ce030230074'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_6'
    name: '6'
    id: 'ev-a9789bf0b61362cc'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'IaC_Generator'
    name: 'IaC-Generator'
    id: 'ev-702ad9ca95500d26'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_7'
    name: '7'
    id: 'ev-b601b4a18aff5358'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Validation_What_if'
    name: 'Validation--What-if'
    id: 'ev-45a98f96cdedf75a'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'OUTPUTS'
    name: 'OUTPUTS'
    id: 'ev-10f715d534504b3f'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Bicep'
    name: 'Bicep'
    id: 'ev-a9cc395f52156f2a'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Terraform'
    name: 'Terraform'
    id: 'ev-251cc5e33f8e50bb'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Missing_Questions'
    name: 'Missing-Questions'
    id: 'ev-053364081ccf1d13'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_1'
    name: '1'
    id: 'ev-49d8ad23a31fe75a'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_2'
    name: '2'
    id: 'ev-9271f02c7a3e1fee'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_3'
    name: '3'
    id: 'ev-9df26ce2dcab0b9d'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_4'
    name: '4'
    id: 'ev-5ae69cbea5c5261e'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Azure'
    name: 'Azure-------'
    id: 'ev-79b5d0e5cc3a93f7'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_5'
    name: '5'
    id: 'ev-c5b7991fccb16809'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_6'
    name: '6'
    id: 'ev-9a67d2d37b41d695'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'VLM_Reconciliation'
    name: 'VLM--Reconciliation'
    id: 'ev-7cbc88cd96c6a8ed'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Editable_source'
    name: 'Editable-source--'
    id: 'ev-ebbd478b8f7a2849'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Document_layout_parsing'
    name: 'Document-layout-parsing'
    id: 'ev-703d62295cf7cc42'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'UI_to_code_sketch_to_code'
    name: 'UI-to-code--sketch-to-code'
    id: 'ev-371cf735f0d1f61e'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Chart_figure_parsing'
    name: 'Chart--figure-parsing'
    id: 'ev-b550797d7c7cf799'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'draw_io_XML_Parser'
    name: 'drawio-XML-Parser'
    id: 'ev-4872fd13e296de91'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'PowerPoint_Shape_Parser'
    name: 'PowerPoint-Shape-Parser'
    id: 'ev-4879959b8399fcc7'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Azure_Icon_Classifier'
    name: 'Azure-Icon-Classifier'
    id: 'ev-f4a3c9b59e4060ac'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Connector_Arrow_Resolver'
    name: 'Connector--Arrow-Resolver'
    id: 'ev-bf1cbc4cca912816'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'element_json'
    name: 'elementjson'
    id: 'ev-7d6361efec9a0ed3'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Azure_resource_candidate'
    name: 'Azure-resource-candidate-----'
    id: 'ev-c0d2dcc80aa4e1e2'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Single_Source_of_Truth'
    name: 'Single-Source-of-Truth'
    id: 'ev-ff16e87167a68542'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_40'
    name: '--'
    id: 'ev-456a213bf779bbdd'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_41'
    name: '-'
    id: 'ev-edb12f04880cef96'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Architecture_Graph'
    name: '-Architecture-Graph-'
    id: 'ev-9c8383ad9b883859'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Shape'
    name: '-Shape'
    id: 'ev-36df4f429cc96d31'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Node'
    name: 'Node'
    id: 'ev-8f5783ea5eabe30d'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Arrow'
    name: '-Arrow'
    id: 'ev-98e0e283f1a7dfd9'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Edge'
    name: 'Edge'
    id: 'ev-bd9b11db69e33bc6'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Boundary'
    name: '--Boundary'
    id: 'ev-252adf72f29e851c'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Container'
    name: 'Container'
    id: 'ev-13e6fc7f538e633a'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_49'
    name: '---'
    id: 'ev-24f9a834a2a6c7c9'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_50'
    name: '-'
    id: 'ev-3ac498c28c1f130a'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Dependency_Hint'
    name: 'Dependency-Hint'
    id: 'ev-7f1bb22df6519323'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Legend'
    name: 'Legend'
    id: 'ev-dde102cd4860b80f'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Flow_Meaning'
    name: 'Flow-Meaning'
    id: 'ev-3d1423ae0aa780ad'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_54'
    name: '--'
    id: 'ev-9d0b75493d173ac7'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'External_User'
    name: 'External-User'
    id: 'ev-e06acf93a87273a7'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Conditional_Access'
    name: 'Conditional-Access'
    id: 'ev-1655c34933c2ccb6'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'AVD_Service'
    name: 'AVD-Service'
    id: 'ev-948ca6ea0657d643'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Internal_Servers'
    name: 'Internal-Servers'
    id: 'ev-8654ecc43951369e'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'architecture_ir_json'
    name: 'architectureirjson'
    id: 'ev-93740da57a80363a'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resources'
    name: 'resources'
    id: 'ev-b13d537187a4dc25'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'relationships'
    name: 'relationships'
    id: 'ev-44140de6a223b2bf'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'containers'
    name: 'containers'
    id: 'ev-0837f3898a49ad29'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'securityControls'
    name: 'securityControls'
    id: 'ev-821460e9de454f2d'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'existingResources'
    name: 'existingResources'
    id: 'ev-82d85fa612e2fdb6'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'manualControls'
    name: 'manualControls'
    id: 'ev-5c9af2a83b96bb8c'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'questions'
    name: 'questions'
    id: 'ev-0a6e65bd1aba5a2e'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'warnings'
    name: 'warnings'
    id: 'ev-e0e982e9391554f9'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'confidence_score'
    name: 'confidence-score'
    id: 'ev-8b2a191ef49951e2'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Bicep'
    name: 'Bicep'
    id: 'ev-7e86359723801c12'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Azure_IaC'
    name: 'Azure--IaC'
    id: 'ev-568c69eb3b9dabfa'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Terraform'
    name: 'Terraform'
    id: 'ev-3097478da374711f'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'IaC'
    name: '--IaC'
    id: 'ev-0ca0b9b299dc3a46'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Blocker'
    name: 'Blocker'
    id: 'ev-8f4945a687a94ed5'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_74'
    name: '---'
    id: 'ev-3407d9f53682c433'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Risk'
    name: 'Risk'
    id: 'ev-dda565101ad953a3'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_76'
    name: '---'
    id: 'ev-068beb5249fce997'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Optional'
    name: 'Optional'
    id: 'ev-1088103f947f508e'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_78'
    name: '-'
    id: 'ev-76dd92bf8b431a6d'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Manual_Control'
    name: 'Manual-Control'
    id: 'ev-92d28b098e83c509'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_80'
    name: '-'
    id: 'ev-e1bf92b85bc6d306'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Architecture_IR'
    name: 'Architecture--IR'
    id: 'ev-37a9f0216c77fa60'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'IR_Bicep_emitter'
    name: 'IR--Bicep-emitter'
    id: 'ev-df94997259438d79'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Raw_Bicep_AVM_Azure'
    name: 'Raw-Bicep---AVM-----Azure---'
    id: 'ev-eacb18d3c19d095c'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'IR_Terraform_emitter'
    name: 'IR--Terraform-emitter'
    id: 'ev-9dc00639269eca70'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_85'
    name: '--'
    id: 'ev-db09fc58b82d62c8'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'A'
    name: 'A'
    id: 'ev-a3cc9e195dfba081'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'B'
    name: 'B'
    id: 'ev-b179ad0bacfb3341'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Traceability'
    name: '--Traceability'
    id: 'ev-ae73c20fc5c85a32'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'C'
    name: 'C'
    id: 'ev-b01af9b58dc6f990'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Report'
    name: '-Report--'
    id: 'ev-ef235c7f4643730e'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'architecture_spec_md'
    name: 'architecture-specmd'
    id: 'ev-fcd89a6d6476c37b'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'architecture_spec_docx'
    name: 'architecture-specdocx'
    id: 'ev-a988077c986ba2e4'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'architecture_spec_pdf'
    name: 'architecture-specpdf'
    id: 'ev-701c36826192c86f'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Bicep'
    name: 'Bicep-'
    id: 'ev-28df8267b486880b'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'bicep_format'
    name: 'bicep-format'
    id: 'ev-b1d25e8f9922d710'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'bicep_lint'
    name: 'bicep-lint'
    id: 'ev-be5664a1e4ab8a34'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'bicep_build'
    name: 'bicep-build'
    id: 'ev-8fc4a1ffcee7e24e'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'az_deployment_validate'
    name: 'az-deployment-validate'
    id: 'ev-949fc8d3aa6d8702'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'az_deployment_what_if'
    name: 'az-deployment-what-if'
    id: 'ev-a8ec92c41556d6a9'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Terraform'
    name: 'Terraform-'
    id: 'ev-4aa2919b6d82f922'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'terraform_fmt'
    name: 'terraform-fmt'
    id: 'ev-bac1e199ccc4398f'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'terraform_validate'
    name: 'terraform-validate'
    id: 'ev-b75a4eb42622293b'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'tflint'
    name: 'tflint'
    id: 'ev-656e0263d41e5755'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'terraform_plan'
    name: 'terraform-plan'
    id: 'ev-9b82d0aa671bb665'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'validation_report_md'
    name: 'validation-reportmd'
    id: 'ev-f04e23744c15bfa5'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'unresolved_questions_md'
    name: 'unresolved-questionsmd'
    id: 'ev-ca73c9998b44abad'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'deployment_plan_md'
    name: 'deployment-planmd'
    id: 'ev-8ce585c0a1ee573d'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_1_MVP'
    name: '-1-MVP'
    id: 'ev-f383eb5a70c19f0f'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_109'
    name: 'resource-109'
    id: 'ev-fa085a6443b36d7f'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'draw_io_XML'
    name: 'drawio-XML'
    id: 'ev-3ae46715a0318334'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'PowerPoint_PPTX'
    name: 'PowerPoint-PPTX'
    id: 'ev-754816c008d169e9'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'PNG'
    name: 'PNG-'
    id: 'ev-603454d62d891b8a'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_113'
    name: '-'
    id: 'ev-05393605497f67e6'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Log_Analytics_Diagnostic_Settings'
    name: 'Log-Analytics--Diagnostic-Settings'
    id: 'ev-872c8b50ea71db02'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_115'
    name: 'resource-115'
    id: 'ev-2aff140c18c3ac5b'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'architecture_ir_json'
    name: 'architectureirjson'
    id: 'ev-80f090052a105705'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'detected_elements_csv'
    name: 'detected-elementscsv'
    id: 'ev-baab45d89a312a81'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'iac_readiness_report_md'
    name: 'iac-readiness-reportmd'
    id: 'ev-9a8ab69f9426cdbd'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'main_bicep'
    name: 'mainbicep'
    id: 'ev-cd3754d63177df63'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'validation_report_md'
    name: 'validation-reportmd'
    id: 'ev-4a632d5f73a5efc8'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'resource_121'
    name: '--'
    id: 'ev-b72eee3125d23ba6'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_1'
    name: '1'
    id: 'ev-c454084edba05fdb'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Phase_1'
    name: 'Phase-1'
    id: 'ev-b01a59642b45ff2d'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_2'
    name: '2'
    id: 'ev-75063b4af078270f'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Phase_2'
    name: 'Phase-2'
    id: 'ev-4952abc4b205dfc0'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_3'
    name: '3'
    id: 'ev-c8b116c895f459a6'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Phase_3'
    name: 'Phase-3'
    id: 'ev-b0613666adf2a906'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Bicep_Generator'
    name: 'Bicep-Generator'
    id: 'ev-41d7f059e1a75144'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_4'
    name: '4'
    id: 'ev-a0fbc24de90b45fd'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Phase_4'
    name: 'Phase-4'
    id: 'ev-f6649a9e6be1efcb'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Validation_What_if'
    name: 'Validation--What-if'
    id: 'ev-dda2e00fdc953ab3'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_5'
    name: '5'
    id: 'ev-edccc52ad07c11df'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Phase_5'
    name: 'Phase-5'
    id: 'ev-514696209c5b20af'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Terraform_Generator'
    name: 'Terraform-Generator'
    id: 'ev-fbe0c871caaaba03'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_6'
    name: '6'
    id: 'ev-9bbfbddbf39f4ebd'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Phase_6'
    name: 'Phase-6'
    id: 'ev-90c32e05753fc69e'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'r_7'
    name: '7'
    id: 'ev-8eadd238b73c8eef'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Phase_7'
    name: 'Phase-7'
    id: 'ev-05deff7ed6b11209'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'GitHub_Actions_Azure_DevOps_PR'
    name: 'GitHub-Actions--Azure-DevOps-PR-'
    id: 'ev-0fb007f65c197bc3'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'IaC_Generator'
    name: 'IaC--Generator'
    id: 'ev-43615029073ebf9a'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
  {
    symbolicName: 'Validation_Automation'
    name: 'Validation--Automation'
    id: 'ev-a9a95e62cb7c4a93'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
]

@description('Draft architecture relationships extracted from source diagrams.')
var inferredRelationships = [
  {
    id: 'ev-f294fc68ec30c8a6'
    from: 'ev-e7bbd27415313083'
    to: 'ev-f37f516dcc2283f7'
    kind: 'dependency'
  }
  {
    id: 'ev-6907beb8ef5e2047'
    from: 'ev-d75715e51f99c0a2'
    to: 'ev-bfd5f1f4d71ab858'
    kind: 'dependency'
  }
  {
    id: 'ev-8dcb1b0897f09e14'
    from: 'ev-de7160a40eb9223f'
    to: 'ev-5fc729aa7775f648'
    kind: 'dependency'
  }
  {
    id: 'ev-77c3cc49a7491253'
    from: 'ev-1dc24dbc285f24c0'
    to: 'ev-9b9c59e7d5f40a9c'
    kind: 'dependency'
  }
  {
    id: 'ev-3db259741211d84f'
    from: 'ev-43d26d357ccb054b'
    to: 'ev-22f7448237e4d4c8'
    kind: 'dependency'
  }
  {
    id: 'ev-959b0ba5386a4a38'
    from: 'ev-22f7448237e4d4c8'
    to: 'ev-89d21ce030230074'
    kind: 'dependency'
  }
  {
    id: 'ev-8c6ff4142e381624'
    from: 'ev-5149950fac6a6cbe'
    to: 'ev-a9789bf0b61362cc'
    kind: 'dependency'
  }
  {
    id: 'ev-b36e6b94371dde32'
    from: 'ev-97dd4242e290ade5'
    to: 'ev-b601b4a18aff5358'
    kind: 'dependency'
  }
  {
    id: 'ev-0dc9d5f8e42a0c50'
    from: 'ev-ae0b0374064523e0'
    to: 'ev-38fbb44d8b75b83c'
    kind: 'dependency'
  }
  {
    id: 'ev-d3f2336541638193'
    from: 'ev-38fbb44d8b75b83c'
    to: 'ev-7cbc88cd96c6a8ed'
    kind: 'dependency'
  }
  {
    id: 'ev-479fc7cd3ac042eb'
    from: 'ev-38fbb44d8b75b83c'
    to: 'ev-7cbc88cd96c6a8ed'
    kind: 'dependency'
  }
  {
    id: 'ev-af400eeedec84811'
    from: 'ev-38fbb44d8b75b83c'
    to: 'ev-7cbc88cd96c6a8ed'
    kind: 'dependency'
  }
  {
    id: 'ev-a740bc3b6ba68e82'
    from: 'ev-4b70d44e2235fc34'
    to: 'ev-8f5783ea5eabe30d'
    kind: 'dependency'
  }
  {
    id: 'ev-24ecb66426564988'
    from: 'ev-4c4a04841ff0c53f'
    to: 'ev-bd9b11db69e33bc6'
    kind: 'dependency'
  }
  {
    id: 'ev-f40f4abbe413efe7'
    from: 'ev-d99023addee30b43'
    to: 'ev-05b5c858c3d0b17e'
    kind: 'dependency'
  }
  {
    id: 'ev-1da45ba0d9af2176'
    from: 'ev-123037a38e0505fe'
    to: 'ev-de30f80af95ac432'
    kind: 'dependency'
  }
  {
    id: 'ev-867f0dccc910a4c8'
    from: 'ev-f941c11b12b684f2'
    to: 'ev-7f1bb22df6519323'
    kind: 'dependency'
  }
  {
    id: 'ev-1a874d0e8072d169'
    from: 'ev-4b5b5383ee0ff7cf'
    to: 'ev-3d1423ae0aa780ad'
    kind: 'dependency'
  }
  {
    id: 'ev-c3867fe44d1aeabc'
    from: 'ev-859278d797dd8b9e'
    to: 'ev-e7fc89e9b02929f8'
    kind: 'dependency'
  }
  {
    id: 'ev-082231873dc88dc7'
    from: 'ev-1e4af984ab71abd2'
    to: 'ev-1655c34933c2ccb6'
    kind: 'dependency'
  }
  {
    id: 'ev-c0727de664f6cf8f'
    from: 'ev-9d0b75493d173ac7'
    to: 'ev-29fc7ca9e431f666'
    kind: 'dependency'
  }
  {
    id: 'ev-8b39a031bbe62368'
    from: 'ev-29fc7ca9e431f666'
    to: 'ev-aa849a22fd1d9541'
    kind: 'dependency'
  }
  {
    id: 'ev-f429a72e8eca1f88'
    from: 'ev-c90e96c65895fdd5'
    to: 'ev-5b256cbfbe787bb7'
    kind: 'dependency'
  }
  {
    id: 'ev-3d0d79f11cd2b7b6'
    from: 'ev-eb721934a01f4f4f'
    to: 'ev-eddfa49f2eafa1e7'
    kind: 'dependency'
  }
  {
    id: 'ev-5bb11a2e11d270ce'
    from: 'ev-eb721934a01f4f4f'
    to: 'ev-eddfa49f2eafa1e7'
    kind: 'dependency'
  }
  {
    id: 'ev-5bad7f7ef6cd3930'
    from: 'ev-8fbf6b636a815cc5'
    to: 'ev-c8e817f3f3d789d5'
    kind: 'dependency'
  }
  {
    id: 'ev-5d4c00419ae49ce1'
    from: 'ev-df138c2af0c0e84e'
    to: 'ev-8cb0a940b44260b1'
    kind: 'dependency'
  }
  {
    id: 'ev-25bd4b4d2a4e1c99'
    from: 'ev-2d4208019a76dc43'
    to: 'ev-a0fbc24de90b45fd'
    kind: 'dependency'
  }
  {
    id: 'ev-da07ce01adb8c289'
    from: 'ev-6158e67a8a72f337'
    to: 'ev-45ca70e28afbc673'
    kind: 'dependency'
  }
  {
    id: 'ev-c17d9f9628a0f18a'
    from: 'ev-45ca70e28afbc673'
    to: 'ev-937c678a5bd004a4'
    kind: 'dependency'
  }
  {
    id: 'ev-fce3fbb1885ef8f9'
    from: 'ev-9d5d1161466e3a8a'
    to: 'ev-487ca8cc3dc21c5b'
    kind: 'dependency'
  }
]

output inferredResourceCount int = length(inferredResources)
output inferredRelationshipCount int = length(inferredRelationships)
