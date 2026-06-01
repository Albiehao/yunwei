export enum ScheduleAction {
  Start = 'start',
  Stop = 'stop'
}

export interface Schedule {
  id: string
  name: string
  serverId: string
  serverName: string
  action: ScheduleAction
  cronExpression: string
  timezone: string
  enabled: boolean
  lastRunAt?: string
  nextRunAt?: string
  createdAt: string
  updatedAt: string
}

export interface ScheduleFormData {
  name: string
  serverId: string
  action: ScheduleAction
  cronExpression: string
  timezone: string
  enabled: boolean
}
