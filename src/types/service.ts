export enum ServiceCategory {
  Storage = 'storage',
  Network = 'network',
  Database = 'database',
  Security = 'security',
  Compute = 'compute'
}

export interface PayAsYouGoService {
  id: string
  name: string
  category: ServiceCategory
  description: string
  enabled: boolean
  serverId?: string
  monthlyCost: number
  status: 'running' | 'stopped' | 'error'
  createdAt: string
}
