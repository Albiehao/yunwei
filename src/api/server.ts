import api from './index'
import type { ApiResponse, Server } from '@/types'

export function getServers(): Promise<ApiResponse<Server[]>> {
  return api.get('/servers')
}

export function getServerById(id: string): Promise<ApiResponse<Server>> {
  return api.get(`/servers/${id}`)
}

export function startServer(id: string): Promise<ApiResponse<null>> {
  return api.post(`/servers/${id}/start`)
}

export function stopServer(id: string): Promise<ApiResponse<null>> {
  return api.post(`/servers/${id}/stop`)
}
