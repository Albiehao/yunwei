import type { MockAdapter } from 'axios-mock-adapter'
import type { Server, PurchaseParams } from '@/types/server'
import type { PayAsYouGoService } from '@/types/service'
import type { Schedule, ScheduleFormData } from '@/types/schedule'
import type { InstanceType } from '@/types/common'
import { ServerStatus } from '@/types/server'
import { ServiceCategory } from '@/types/service'
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

let serviceIdCounter = 0
function nextServiceId() {
  serviceIdCounter++
  return `svc-${String(serviceIdCounter).padStart(4, '0')}`
}

let scheduleIdCounter = 0
function nextScheduleId() {
  scheduleIdCounter++
  return `sch-${String(scheduleIdCounter).padStart(4, '0')}`
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
    name: '测试-ci-01',
    instanceType: 'ecs.g6.large',
    status: ServerStatus.Stopped,
    region: 'cn-shanghai',
    ipAddress: '10.0.4.10',
    spec: { cpu: 4, memory: 8, disk: 40, bandwidth: 50 },
    chargeType: 'PostPaid',
    createdAt: '2026-04-05T03:00:00Z',
    tags: { env: 'testing', role: 'ci' }
  },
  {
    id: nextServerId(),
    name: '中间件-缓存-01',
    instanceType: 'ecs.g6.large',
    status: ServerStatus.Running,
    region: 'cn-hangzhou',
    ipAddress: '10.0.1.20',
    spec: { cpu: 4, memory: 16, disk: 60, bandwidth: 100 },
    chargeType: 'PrePaid',
    createdAt: '2026-01-20T09:00:00Z',
    expiredAt: '2027-01-20T09:00:00Z',
    tags: { env: 'production', role: 'middleware' }
  },
  {
    id: nextServerId(),
    name: '网关-边缘-01',
    instanceType: 'ecs.g6.xlarge',
    status: ServerStatus.Running,
    region: 'cn-hangzhou',
    ipAddress: '10.0.1.1',
    spec: { cpu: 8, memory: 16, disk: 40, bandwidth: 500 },
    chargeType: 'PrePaid',
    createdAt: '2025-12-01T00:00:00Z',
    expiredAt: '2026-12-01T00:00:00Z',
    tags: { env: 'production', role: 'gateway' }
  },
  {
    id: nextServerId(),
    name: '日志-采集-01',
    instanceType: 'ecs.g6.medium',
    status: ServerStatus.Running,
    region: 'cn-shanghai',
    ipAddress: '10.0.4.5',
    spec: { cpu: 2, memory: 4, disk: 500, bandwidth: 100 },
    chargeType: 'PostPaid',
    createdAt: '2026-05-01T12:00:00Z',
    tags: { env: 'production', role: 'logging' }
  }
]

const services: PayAsYouGoService[] = [
  {
    id: nextServiceId(),
    name: 'OSS 对象存储',
    category: ServiceCategory.Storage,
    description: '海量、安全、低成本的云存储服务',
    enabled: true,
    monthlyCost: 35.5,
    status: 'running',
    createdAt: '2026-01-01T00:00:00Z'
  },
  {
    id: nextServiceId(),
    name: 'CDN 加速',
    category: ServiceCategory.Network,
    description: '全球加速内容分发网络',
    enabled: true,
    monthlyCost: 120.0,
    status: 'running',
    createdAt: '2026-01-10T00:00:00Z'
  },
  {
    id: nextServiceId(),
    name: 'RDS 数据库',
    category: ServiceCategory.Database,
    description: '关系型数据库服务',
    enabled: true,
    serverId: servers[2].id,
    monthlyCost: 256.0,
    status: 'running',
    createdAt: '2025-11-20T06:00:00Z'
  },
  {
    id: nextServiceId(),
    name: 'WAF Web应用防火墙',
    category: ServiceCategory.Security,
    description: 'Web应用防护服务',
    enabled: false,
    monthlyCost: 88.0,
    status: 'stopped',
    createdAt: '2026-02-15T00:00:00Z'
  },
  {
    id: nextServiceId(),
    name: 'SLB 负载均衡',
    category: ServiceCategory.Network,
    description: '流量分发与负载均衡服务',
    enabled: true,
    monthlyCost: 45.0,
    status: 'running',
    createdAt: '2026-01-15T08:00:00Z'
  },
  {
    id: nextServiceId(),
    name: '弹性伸缩',
    category: ServiceCategory.Compute,
    description: '根据业务负载自动调整计算资源',
    enabled: false,
    monthlyCost: 0,
    status: 'stopped',
    createdAt: '2026-03-01T00:00:00Z'
  },
  {
    id: nextServiceId(),
    name: '云监控',
    category: ServiceCategory.Compute,
    description: '全方位云资源监控与告警',
    enabled: true,
    monthlyCost: 15.0,
    status: 'running',
    createdAt: '2026-01-01T00:00:00Z'
  },
  {
    id: nextServiceId(),
    name: 'DDoS 防护',
    category: ServiceCategory.Security,
    description: 'DDoS攻击防护服务',
    enabled: true,
    monthlyCost: 60.0,
    status: 'running',
    createdAt: '2026-02-01T00:00:00Z'
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
    name: '周末全天开机',
    serverId: servers[1].id,
    serverName: servers[1].name,
    action: ScheduleAction.Start,
    cronExpression: '0 6 * * 6,7',
    timezone: 'Asia/Shanghai',
    enabled: false,
    createdAt: '2026-02-10T00:00:00Z',
    updatedAt: '2026-02-10T00:00:00Z'
  },
  {
    id: nextScheduleId(),
    name: '数据库备份前开机',
    serverId: servers[2].id,
    serverName: servers[2].name,
    action: ScheduleAction.Start,
    cronExpression: '0 2 * * *',
    timezone: 'Asia/Shanghai',
    enabled: true,
    lastRunAt: '2026-06-01T02:00:00Z',
    nextRunAt: '2026-06-02T02:00:00Z',
    createdAt: '2025-12-01T00:00:00Z',
    updatedAt: '2025-12-01T00:00:00Z'
  },
  {
    id: nextScheduleId(),
    name: '测试环境日间开机',
    serverId: servers[4].id,
    serverName: servers[4].name,
    action: ScheduleAction.Start,
    cronExpression: '0 9 * * 1-5',
    timezone: 'Asia/Shanghai',
    enabled: true,
    lastRunAt: '2026-05-31T09:00:00Z',
    nextRunAt: '2026-06-01T09:00:00Z',
    createdAt: '2026-04-05T03:00:00Z',
    updatedAt: '2026-04-05T03:00:00Z'
  },
  {
    id: nextScheduleId(),
    name: '开发环境关机',
    serverId: servers[3].id,
    serverName: servers[3].name,
    action: ScheduleAction.Stop,
    cronExpression: '0 20 * * 1-5',
    timezone: 'Asia/Shanghai',
    enabled: false,
    createdAt: '2026-03-10T02:00:00Z',
    updatedAt: '2026-03-10T02:00:00Z'
  }
]

const instanceTypes: InstanceType[] = [
  {
    id: 'ecs.g6.medium',
    name: '通用型 g6 - 2vCPU 4GB',
    cpu: 2,
    memory: 4,
    disk: 20,
    bandwidth: 50,
    hourlyPrice: 0.42,
    monthlyPrice: 302.4,
    family: 'g6',
    description: '通用型实例，适合中小型应用'
  },
  {
    id: 'ecs.g6.large',
    name: '通用型 g6 - 4vCPU 8GB',
    cpu: 4,
    memory: 8,
    disk: 40,
    bandwidth: 100,
    hourlyPrice: 0.84,
    monthlyPrice: 604.8,
    family: 'g6',
    description: '通用型实例，适合标准应用和微服务'
  },
  {
    id: 'ecs.g6.xlarge',
    name: '通用型 g6 - 8vCPU 16GB',
    cpu: 8,
    memory: 16,
    disk: 80,
    bandwidth: 200,
    hourlyPrice: 1.68,
    monthlyPrice: 1209.6,
    family: 'g6',
    description: '通用型实例，适合中大型应用'
  },
  {
    id: 'ecs.r6.xlarge',
    name: '内存型 r6 - 8vCPU 32GB',
    cpu: 8,
    memory: 32,
    disk: 200,
    bandwidth: 100,
    hourlyPrice: 2.1,
    monthlyPrice: 1512.0,
    family: 'r6',
    description: '内存密集型实例，适合数据库和缓存'
  },
  {
    id: 'ecs.c6.xlarge',
    name: '计算型 c6 - 8vCPU 16GB',
    cpu: 8,
    memory: 16,
    disk: 40,
    bandwidth: 200,
    hourlyPrice: 1.52,
    monthlyPrice: 1094.4,
    family: 'c6',
    description: '计算密集型实例，适合批处理和高性能计算'
  },
  {
    id: 'ecs.g7.large',
    name: '通用型 g7 - 4vCPU 8GB',
    cpu: 4,
    memory: 8,
    disk: 40,
    bandwidth: 150,
    hourlyPrice: 0.92,
    monthlyPrice: 662.4,
    family: 'g7',
    description: '新一代通用型实例，性能提升20%'
  }
]

function wrap<T>(data: T) {
  return { code: 200, message: 'success', data }
}

function notFound(id: string) {
  return { code: 404, message: `Resource not found: ${id}`, data: null }
}

export default function setupMock(mock: MockAdapter) {
  // ---- Servers ----

  mock.onGet('/api/servers').reply(async () => {
    await randomDelay()
    return [200, wrap([...servers])]
  })

  mock.onPost(/\/api\/servers\/([^/]+)\/start/).reply(async (config) => {
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

  mock.onPost(/\/api\/servers\/([^/]+)\/stop/).reply(async (config) => {
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

  // ---- Services ----

  mock.onGet('/api/services').reply(async () => {
    await randomDelay()
    return [200, wrap([...services])]
  })

  mock.onPut(/\/api\/services\/([^/]+)/).reply(async (config) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/services\/([^/]+)/)![1]
    const body = JSON.parse(config.data || '{}')
    const service = services.find((s) => s.id === id)
    if (!service) return [404, notFound(id)]
    Object.assign(service, body)
    return [200, wrap({ ...service })]
  })

  // ---- Schedules ----

  mock.onGet('/api/schedules').reply(async () => {
    await randomDelay()
    return [200, wrap([...schedules])]
  })

  mock.onPost('/api/schedules').reply(async (config) => {
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

  mock.onPut(/\/api\/schedules\/([^/]+)/).reply(async (config) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/schedules\/([^/]+)/)![1]
    const body = JSON.parse(config.data || '{}')
    const schedule = schedules.find((s) => s.id === id)
    if (!schedule) return [404, notFound(id)]
    Object.assign(schedule, body, { updatedAt: new Date().toISOString() })
    return [200, wrap({ ...schedule })]
  })

  mock.onDelete(/\/api\/schedules\/([^/]+)/).reply(async (config) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/schedules\/([^/]+)/)![1]
    const index = schedules.findIndex((s) => s.id === id)
    if (index === -1) return [404, notFound(id)]
    schedules.splice(index, 1)
    return [200, wrap(null)]
  })

  mock.onPatch(/\/api\/schedules\/([^/]+)\/toggle/).reply(async (config) => {
    await randomDelay()
    const id = config.url!.match(/\/api\/schedules\/([^/]+)\/toggle/)![1]
    const schedule = schedules.find((s) => s.id === id)
    if (!schedule) return [404, notFound(id)]
    schedule.enabled = !schedule.enabled
    schedule.updatedAt = new Date().toISOString()
    return [200, wrap({ ...schedule })]
  })

  // ---- Instance Types ----

  mock.onGet('/api/instance-types').reply(async () => {
    await randomDelay()
    return [200, wrap([...instanceTypes])]
  })

  // ---- Purchase ----

  mock.onPost('/api/purchase').reply(async (config) => {
    await randomDelay()
    const body: PurchaseParams = JSON.parse(config.data || '{}')
    const instance = instanceTypes.find((t) => t.id === body.instanceType)
    const now = new Date().toISOString()
    const server: Server = {
      id: nextServerId(),
      name: body.name,
      instanceType: body.instanceType,
      status: ServerStatus.Pending,
      region: body.region,
      ipAddress: `10.0.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
      spec: {
        cpu: instance?.cpu ?? 2,
        memory: instance?.memory ?? 4,
        disk: instance?.disk ?? 20,
        bandwidth: instance?.bandwidth ?? 50
      },
      chargeType: body.chargeType,
      createdAt: now,
      expiredAt: body.duration
        ? new Date(Date.now() + body.duration * 30 * 24 * 60 * 60 * 1000).toISOString()
        : undefined,
      tags: {}
    }
    servers.unshift(server)
    // Simulate pending -> running transition
    setTimeout(() => {
      server.status = ServerStatus.Running
    }, 3000 + Math.random() * 2000)
    return [200, wrap(server)]
  })
}
