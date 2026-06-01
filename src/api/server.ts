import api from './index'
import type { ApiResponse } from '@/types/common'
import type { Server } from '@/types/server'

export function getServers(): Promise<ApiResponse<Server[]>> {
  return api.get('/servers')
}

export function startServer(id: string): Promise<ApiResponse<null>> {
  return api.post(`/servers/${id}/start`)
}

export function stopServer(id: string): Promise<ApiResponse<null>> {
  return api.post(`/servers/${id}/stop`)
}
