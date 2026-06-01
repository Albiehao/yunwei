import MockAdapter from 'axios-mock-adapter'
import type { Server } from '@/types/server'
import type { Schedule, ScheduleFormData } from '@/types/schedule'
import type { User } from '@/types/common'
import { ServerStatus } from '@/types/server'
import { ScheduleAction } from '@/types/schedule'

function delay(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

function randomDelay() {
  return delay(300 + Math.random() * 500)
}

let serverIdCounter = 0
function nextServerId() {
  serverIdCounter++
  return `i-${String(serverIdCounter).padStart(4, '0')}`
}

let scheduleIdCounter = 0
function nextScheduleId() {
  scheduleIdCounter++
  return `sch-${String(scheduleIdCounter).padStart(4, '0')}`
}

let userIdCounter = 0
function nextUserId() {
  userIdCounter++
  return `u-${String(userIdCounter).padStart(4, '0')}`
}

// ---- Seed data ----

const servers: Server[] = [
  {
    id: nextServerId(),
    name: 'web-生产-01',
    instanceType: 'ecs.g6.large',
    status: ServerStatus.Running,
    region: 'cn-hangzhou',
    ipAddress: '10.0.1.101',
    spec: { cpu: 4, memory: 8, disk: 40, bandwidth: 100 },
    chargeType: 'PrePaid',
    createdAt: '2026-01-15T08:00:00Z',
    expiredAt: '2027-01-15T08:00:00Z',
    tags: { env: 'production', role: 'web' }
  },
  {
    id: nextServerId(),
    name: 'api-核心-01',
    instanceType: 'ecs.g6.xlarge',
    status: ServerStatus.Running,
    region: 'cn-shanghai',
    ipAddress: '10.0.2.12',
    spec: { cpu: 8, memory: 16, disk: 80, bandwidth: 200 },
    chargeType: 'PrePaid',
    createdAt: '2026-02-01T10:00:00Z',
    expiredAt: '2027-02-01T10:00:00Z',
    tags: { env: 'production', role: 'api' }
  },
  {
    id: nextServerId(),
    name: 'dev-开发-01',
    instanceType: 'ecs.g6.medium',
    status: ServerStatus.Stopped,
    region: 'cn-hangzhou',
    ipAddress: '10.0.3.50',
    spec: { cpu: 2, memory: 4, disk: 20, bandwidth: 50 },
    chargeType: 'PostPaid',
    createdAt: '2026-03-10T02:00:00Z',
    tags: { env: 'development', role: 'dev' }
  },
  {
    id: nextServerId(),
    name: '数据库-主库-01',
    instanceType: 'ecs.r6.xlarge',
    status: ServerStatus.Running,
    region: 'cn-hangzhou',
    ipAddress: '10.0.1.5',
    spec: { cpu: 8, memory: 32, disk: 200, bandwidth: 100 },
    chargeType: 'PrePaid',
    createdAt: '2025-11-20T06:00:00Z',
    expiredAt: '2026-11-20T06:00:00Z',
    tags: { env: 'production', role: 'database' }
  },
  {
    id: nextServerId(),
    name: '测试-ci-01',
    instanceType: 'ecs.g6.large',
    status: ServerStatus.Stopped,
    region: 'cn-shanghai',
    ipAddress: '10.0.4.10',
    spec: { cpu: 4, memory: 8, disk: 40, bandwidth: 50 },
    chargeType: 'PostPaid',
    createdAt: '2026-04-05T03:00:00Z',
    tags: { env: 'testing', role: 'ci' }
  }
]

const schedules: Schedule[] = [
  {
    id: nextScheduleId(),
    name: '工作日开机',
    serverId: servers[0].id,
    serverName: servers[0].name,
    action: ScheduleAction.Start,
    cronExpression: '0 8 * * 1-5',
    timezone: 'Asia/Shanghai',
    enabled: true,
    lastRunAt: '2026-05-31T08:00:00Z',
    nextRunAt: '2026-06-01T08:00:00Z',
    createdAt: '2026-01-20T00:00:00Z',
    updatedAt: '2026-01-20T00:00:00Z'
  },
  {
    id: nextScheduleId(),
    name: '晚间关机',
    serverId: servers[0].id,
    serverName: servers[0].name,
    action: ScheduleAction.Stop,
    cronExpression: '0 22 * * 1-5',
    timezone: 'Asia/Shanghai',
    enabled: true,
    lastRunAt: '2026-05-30T22:00:00Z',
    nextRunAt: '2026-06-01T22:00:00Z',
    createdAt: '2026-01-20T00:00:00Z',
    updatedAt: '2026-01-20T00:00:00Z'
  },
  {
    id: nextScheduleId(),
    name: '测试环境日间开机',
    serverId: servers[4].id,
    serverName: servers[4].name,
    action: ScheduleAction.Start,
    cronExpression: '0 9 * * 1-5',
    timezone: 'Asia/Shanghai',
    enabled: false,
    lastRunAt: '2026-05-31T09:00:00Z',
    nextRunAt: '2026-06-01T09:00:00Z',
    createdAt: '2026-04-05T03:00:00Z',
    updatedAt: '2026-04-05T03:00:00Z'
  }
]

// Mock users
const mockUsers: User[] = [
  { id: nextUserId(), username: 'admin', email: 'admin@cloudops.com', role: 'admin', status: 'active', createdAt: '2025-01-01T00:00:00Z', phone: '13800000001' },
  { id: nextUserId(), username: '张三', email: 'zhangsan@cloudops.com', role: 'operator', status: 'active', createdAt: '2025-06-01T00:00:00Z', phone: '13800000002' },
  { id: nextUserId(), username: '李四', email: 'lisi@cloudops.com', role: 'developer', status: 'active', createdAt: '2025-07-15T00:00:00Z', phone: '13800000003' },
  { id: nextUserId(), username: '王五', email: 'wangwu@cloudops.com', role: 'auditor', status: 'disabled', createdAt: '2025-09-01T00:00:00Z', phone: '13800000004' }
]

// Mock auth users (password store)
const authUsers = [
  { ...mockUsers[0], password: 'admin123' },
  { id: 'u-009', username: 'user', email: 'user@cloudops.com', role: 'operator' as const, status: 'active' as const, createdAt: '2026-01-01T00:00:00Z', password: 'user123' }
]

let currentUser: any = null

function wrap<T>(data: T) {
  return { code: 200, message: 'success', data }
}

function notFound(id: string) {
  return { code: 404, message: `Resource not found: ${id}`, data: null }
}

export default function setupMock(mock: MockAdapter) {
  // ---- Auth ----

  mock.onPost('/api/auth/login').reply(async (config: any) => {
    await randomDelay()
    const { username, password } = JSON.parse(config.data || '{}')
    const user = authUsers.find((u) => u.username === username && u.password === password)
    if (!user) {
      return [401, { code: 401, message: '用户名或密码错误', data: null }]
    }
    const { password: _, ...userInfo } = user
    currentUser = userInfo
    const token = `mock-token-${user.id}-${Date.now()}`
    return [200, wrap({ token, user: userInfo })]
  })

  mock.onGet('/api/auth/me').reply(async () => {
    await randomDelay()
    if (!currentUser) {
      return [401, { code: 401, message: '未登录', data: null }]
    }
    return [200, wrap({ ...currentUser })]
  })

  // ---- Users ----

  mock.onGet('/api/users').reply(async () => {
    await randomDelay()
    return [200, wrap([...mockUsers])]
  })

  mock.onPost('/api/users').reply(async (config: any) => {
    await randomDelay()
    const body = JSON.parse(config.data || '{}')
    const now = new Date().toISOString()
    const user: User = {
      id: nextUserId(),
      username: body.username,
      email: body.email || '',
      role: body.role || 'developer',
      status: body.status || 'active',
      createdAt: now,
      phone: body.phone
    }
    mockUsers.push(user)
    return [200, wrap(user)]
  })

  mock.onPut(/\/api\/users\/([^/]+)/).reply(async (config: any) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/users\/([^/]+)/)![1]
    const body = JSON.parse(config.data || '{}')
    const user = mockUsers.find((u) => u.id === id)
    if (!user) return [404, notFound(id)]
    Object.assign(user, body)
    return [200, wrap({ ...user })]
  })

  mock.onDelete(/\/api\/users\/([^/]+)/).reply(async (config: any) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/users\/([^/]+)/)![1]
    const index = mockUsers.findIndex((u) => u.id === id)
    if (index === -1) return [404, notFound(id)]
    mockUsers.splice(index, 1)
    return [200, wrap(null)]
  })

  // ---- Servers ----

  mock.onGet('/api/servers').reply(async () => {
    await randomDelay()
    return [200, wrap([...servers])]
  })

  mock.onPost(/\/api\/servers\/([^/]+)\/start/).reply(async (config: any) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/servers\/([^/]+)\/start/)![1]
    const server = servers.find((s) => s.id === id)
    if (!server) return [404, notFound(id)]
    if (server.status === ServerStatus.Running) return [200, wrap({ success: true })]
    server.status = ServerStatus.Starting
    setTimeout(() => {
      server.status = ServerStatus.Running
    }, 2000 + Math.random() * 1000)
    return [200, wrap({ success: true })]
  })

  mock.onPost(/\/api\/servers\/([^/]+)\/stop/).reply(async (config: any) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/servers\/([^/]+)\/stop/)![1]
    const server = servers.find((s) => s.id === id)
    if (!server) return [404, notFound(id)]
    if (server.status === ServerStatus.Stopped) return [200, wrap({ success: true })]
    server.status = ServerStatus.Stopping
    setTimeout(() => {
      server.status = ServerStatus.Stopped
    }, 2000 + Math.random() * 1000)
    return [200, wrap({ success: true })]
  })

  // ---- Schedules ----

  mock.onGet('/api/schedules').reply(async () => {
    await randomDelay()
    return [200, wrap([...schedules])]
  })

  mock.onPost('/api/schedules').reply(async (config: any) => {
    await randomDelay()
    const body: ScheduleFormData = JSON.parse(config.data || '{}')
    const now = new Date().toISOString()
    const schedule: Schedule = {
      id: nextScheduleId(),
      name: body.name,
      serverId: body.serverId,
      serverName: servers.find((s) => s.id === body.serverId)?.name || body.serverId,
      action: body.action,
      cronExpression: body.cronExpression,
      timezone: body.timezone,
      enabled: body.enabled,
      createdAt: now,
      updatedAt: now
    }
    schedules.push(schedule)
    return [200, wrap(schedule)]
  })

  mock.onPut(/\/api\/schedules\/([^/]+)/).reply(async (config: any) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/schedules\/([^/]+)/)![1]
    const body = JSON.parse(config.data || '{}')
    const schedule = schedules.find((s) => s.id === id)
    if (!schedule) return [404, notFound(id)]
    Object.assign(schedule, body, { updatedAt: new Date().toISOString() })
    return [200, wrap({ ...schedule })]
  })

  mock.onDelete(/\/api\/schedules\/([^/]+)/).reply(async (config: any) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/schedules\/([^/]+)/)![1]
    const index = schedules.findIndex((s) => s.id === id)
    if (index === -1) return [404, notFound(id)]
    schedules.splice(index, 1)
    return [200, wrap(null)]
  })

  mock.onPatch(/\/api\/schedules\/([^/]+)\/toggle/).reply(async (config: any) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/schedules\/([^/]+)\/toggle/)![1]
    const schedule = schedules.find((s) => s.id === id)
    if (!schedule) return [404, notFound(id)]
    schedule.enabled = !schedule.enabled
    schedule.updatedAt = new Date().toISOString()
    return [200, wrap({ ...schedule })]
  })
}
