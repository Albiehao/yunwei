import api from './index'
import type { ApiResponse, PayAsYouGoService } from '@/types'

export function getServices(): Promise<ApiResponse<PayAsYouGoService[]>> {
  return api.get('/services')
}

export function updateService(id: string, data: Partial<PayAsYouGoService>): Promise<ApiResponse<PayAsYouGoService>> {
  return api.put(`/services/${id}`, data)
}
