import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor - attach auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor - unwrap data
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const detail = error.response?.data?.detail
    const message = error.response?.data?.message || detail || error.message || '请求失败'

    // 401 → redirect to login
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    console.error('API Error:', message)
    return Promise.reject(error)
  }
)

export default api
