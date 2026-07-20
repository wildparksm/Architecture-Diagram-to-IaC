targetScope = 'resourceGroup'

@description('Draft output generated from architecture IR. Not deployment-ready without review.')
param location string = resourceGroup().location

@description('Safe subset of recognized Azure resources emitted as scaffold declarations.')
@description('Draft architecture resources extracted from source diagrams.')
var inferredResources = [
  {
    symbolicName: 'Web'
    name: 'Web'
    id: 'ev-261dfa7e00b5d765'
    category: 'unknown'
    provider: 'neutral'
    deployability: 'DOCUMENTATION_ONLY'
  }
]

@description('Draft architecture relationships extracted from source diagrams.')
var inferredRelationships = [
  {
    id: 'ev-d251a875e566d6df'
    from: 'ev-261dfa7e00b5d765'
    to: 'ev-7e75f86bfe7444c4'
    kind: 'dependency'
  }
]

output inferredResourceCount int = length(inferredResources)
output inferredRelationshipCount int = length(inferredRelationships)
