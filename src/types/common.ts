export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface PaginatedData<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

export interface InstanceType {
  id: string
  name: string
  cpu: number
  memory: number
  disk: number
  bandwidth: number
  hourlyPrice: number
  monthlyPrice: number
  family: string
  description: string
}

export interface Region {
  id: string
  name: string
  label: string
}

export type ChargeType = 'PostPaid' | 'PrePaid'
