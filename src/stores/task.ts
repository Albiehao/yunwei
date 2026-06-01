import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface TaskItem {
  id: number
  action: string
  serverId: string
  serverName: string
  status: 'pending' | 'done' | 'failed'
  message: string
  createdAt: string
  doneAt: string
  params?: Record<string, any>
}

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<TaskItem[]>([])
  const loading = ref(false)

  async function fetchTasks() {
    loading.value = true
    try {
      const token = localStorage.getItem('token')
      const res = await fetch('/api/tasks', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const d = await res.json()
      tasks.value = d.data || []
    } catch {}
    loading.value = false
  }

  async function createRelease(serverId: string, serverName: string) {
    const token = localStorage.getItem('token')
    await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ action: 'release', serverId, serverName })
    })
    await fetchTasks()
  }

  async function executeTask(taskId: number) {
    const token = localStorage.getItem('token')
    const res = await fetch(`/api/tasks/${taskId}/execute`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    })
    const d = await res.json()
    await fetchTasks()
    return d
  }

  async function deleteTask(taskId: number) {
    const token = localStorage.getItem('token')
    await fetch(`/api/tasks/${taskId}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
    await fetchTasks()
  }

  return { tasks, loading, fetchTasks, createRelease, executeTask, deleteTask }
})
