import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
import setupMock from './mock'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Response interceptor - unwrap data
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '请求失败'
    console.error('API Error:', message)
    return Promise.reject(error)
  }
)

// Setup mock synchronously (before any API calls)
if (import.meta.env.VITE_USE_MOCK === 'true') {
  const mock = new MockAdapter(api, { delayResponse: 500 })
  setupMock(mock)
  console.log('[Mock] Mock adapter enabled')
}

export default api
