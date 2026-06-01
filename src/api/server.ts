import api from './index'
import type { ApiResponse } from '@/types/common'
import type { Server } from '@/types/server'

export function getServers(region?: string): Promise<ApiResponse<Server[]>> {
  const params = region ? { region } : {}
  return api.get('/servers', { params })
}

export function startServer(id: string): Promise<ApiResponse<null>> {
  return api.post(`/servers/${id}/start`)
}

export function stopServer(id: string, mode: string = 'KeepCharging'): Promise<ApiResponse<null>> {
  return api.post(`/servers/${id}/stop`, { mode })
}

export function releaseServer(id: string): Promise<ApiResponse<null>> {
  return api.post(`/servers/${id}/release`)
}

export function updateServer(id: string, data: { remark?: string }): Promise<ApiResponse<any>> {
  return api.put(`/servers/${id}`, data)
}
