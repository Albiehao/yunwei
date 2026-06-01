import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Server } from '@/types'
import { ServerStatus } from '@/types'
import { getServers, startServer, stopServer } from '@/api/server'

export const useServerStore = defineStore('server', () => {
  const servers = ref<Server[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const runningServers = computed(() =>
    servers.value.filter(s => s.status === ServerStatus.Running)
  )
  const stoppedServers = computed(() =>
    servers.value.filter(s => s.status === ServerStatus.Stopped)
  )
  const serverCount = computed(() => servers.value.length)

  function serverById(id: string) {
    return servers.value.find(s => s.id === id)
  }

  async function fetchServers() {
    loading.value = true
    error.value = null
    try {
      const res = await getServers()
      servers.value = res.data
    } catch (e: any) {
      error.value = e.message || '获取服务器列表失败'
    } finally {
      loading.value = false
    }
  }

  async function startServerAction(id: string) {
    const server = servers.value.find(s => s.id === id)
    if (!server) return
    server.status = ServerStatus.Starting
    try {
      await startServer(id)
      server.status = ServerStatus.Running
    } catch (e: any) {
      server.status = ServerStatus.Error
      error.value = e.message || '启动失败'
    }
  }

  async function stopServerAction(id: string) {
    const server = servers.value.find(s => s.id === id)
    if (!server) return
    server.status = ServerStatus.Stopping
    try {
      await stopServer(id)
      server.status = ServerStatus.Stopped
    } catch (e: any) {
      server.status = ServerStatus.Error
      error.value = e.message || '停止失败'
    }
  }

  return {
    servers, loading, error,
    runningServers, stoppedServers, serverCount, serverById,
    fetchServers, startServerAction, stopServerAction
  }
})
