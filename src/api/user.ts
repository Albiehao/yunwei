import api from './index'
import type { ApiResponse } from '@/types/common'
import type { User } from '@/types/common'

export function getUsers(): Promise<ApiResponse<User[]>> {
  return api.get('/users')
}

export function createUser(data: Partial<User>): Promise<ApiResponse<User>> {
  return api.post('/users', data)
}

export function updateUser(id: string, data: Partial<User>): Promise<ApiResponse<User>> {
  return api.put(`/users/${id}`, data)
}

export function deleteUser(id: string): Promise<ApiResponse<null>> {
  return api.delete(`/users/${id}`)
}
