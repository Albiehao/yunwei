export enum ServerStatus {
  Running = 'running',
  Stopped = 'stopped',
  Starting = 'starting',
  Stopping = 'stopping',
  Pending = 'pending',
  Error = 'error'
}

export interface ServerSpec {
  cpu: number
  memory: number
  disk: number
  bandwidth: number
}

export interface Server {
  id: string
  name: string
  instanceType: string
  status: ServerStatus
  region: string
  ipAddress: string
  spec: ServerSpec
  chargeType: 'PostPaid' | 'PrePaid'
  createdAt: string
  expiredAt?: string
  tags?: Record<string, string>
}

