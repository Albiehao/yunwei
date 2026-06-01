import api from './index'
import type { ApiResponse, InstanceType, Server, PurchaseParams } from '@/types'

export function getInstanceTypes(): Promise<ApiResponse<InstanceType[]>> {
  return api.get('/instance-types')
}

export function purchaseServer(data: PurchaseParams): Promise<ApiResponse<Server>> {
  return api.post('/purchase', data)
}
