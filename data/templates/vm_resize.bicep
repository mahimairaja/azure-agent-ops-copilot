param vmName string
param location string = resourceGroup().location
param vmSize string = 'Standard_D4s_v3'

resource vm 'Microsoft.Compute/virtualMachines@2021-03-01' existing = {
  name: vmName
}

resource vmUpdate 'Microsoft.Compute/virtualMachines@2021-03-01' = {
  name: vmName
  location: location
  properties: {
    hardwareProfile: {
      vmSize: vmSize
    }
  }
}
