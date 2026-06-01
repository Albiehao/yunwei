import api from './index'
import type { ApiResponse } from '@/types/common'

export interface LoginParams { username: string; password: string }
export interface AuthResult { token: string; user: { id: string; username: string; role: string; avatar: string } }
export interface ApiUser { id: string; username: string; email: string; role: string; status: string; createdAt: string }

export function login(data: LoginParams): Promise<ApiResponse<AuthResult>> {
  return api.post('/auth/login', data)
}

export function getMe(): Promise<ApiResponse<AuthResult['user']>> {
  return api.get('/auth/me')
}
