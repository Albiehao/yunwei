import api from './index'
import type { ApiResponse, Schedule, ScheduleFormData } from '@/types'

export function getSchedules(): Promise<ApiResponse<Schedule[]>> {
  return api.get('/schedules')
}

export function createSchedule(data: ScheduleFormData): Promise<ApiResponse<Schedule>> {
  return api.post('/schedules', data)
}

export function updateSchedule(id: string, data: Partial<ScheduleFormData>): Promise<ApiResponse<Schedule>> {
  return api.put(`/schedules/${id}`, data)
}

export function deleteSchedule(id: string): Promise<ApiResponse<null>> {
  return api.delete(`/schedules/${id}`)
}

export function toggleSchedule(id: string, enabled: boolean): Promise<ApiResponse<Schedule>> {
  return api.patch(`/schedules/${id}/toggle`, { enabled })
}
