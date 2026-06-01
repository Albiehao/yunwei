export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface User {
  id: string
  username: string
  email: string
  role: 'admin' | 'operator' | 'developer' | 'auditor'
  status: 'active' | 'disabled'
  createdAt: string
  phone?: string
}
