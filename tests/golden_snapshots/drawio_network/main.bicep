targetScope = 'resourceGroup'

@description('Draft output generated from architecture IR. Not deployment-ready without review.')
param location string = resourceGroup().location

@description('Safe subset of recognized Azure resources emitted as scaffold declarations.')
@description('Draft architecture resources extracted from source diagrams.')
var inferredResources = [
  {
    symbolicName: 'Web'
    name: 'Web'
    id: 'ev-7590230317b0986d'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
]

@description('Draft architecture relationships extracted from source diagrams.')
var inferredRelationships = [
  {
    id: 'ev-e8bc1bf85f06ee06'
    from: 'ev-7590230317b0986d'
    to: 'ev-2c23918dffebbab3'
    kind: 'dependency'
  }
]

output inferredResourceCount int = length(inferredResources)
output inferredRelationshipCount int = length(inferredRelationships)
