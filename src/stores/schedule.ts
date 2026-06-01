import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Schedule, ScheduleFormData } from '@/types'
import { getSchedules, createSchedule, updateSchedule, deleteSchedule, toggleSchedule } from '@/api/schedule'

export const useScheduleStore = defineStore('schedule', () => {
  const schedules = ref<Schedule[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const enabledSchedules = computed(() => schedules.value.filter(s => s.enabled))

  async function fetchSchedules() {
    loading.value = true
    error.value = null
    try {
      const res = await getSchedules()
      schedules.value = res.data
    } catch (e: any) {
      error.value = e.message || '获取定时任务失败'
    } finally {
      loading.value = false
    }
  }

  async function createScheduleAction(data: ScheduleFormData) {
    try {
      const res = await createSchedule(data)
      schedules.value.push(res.data)
    } catch (e: any) {
      error.value = e.message || '创建定时任务失败'
      throw e
    }
  }

  async function updateScheduleAction(id: string, data: Partial<ScheduleFormData>) {
    try {
      await updateSchedule(id, data)
      const idx = schedules.value.findIndex(s => s.id === id)
      if (idx !== -1) {
        schedules.value[idx] = { ...schedules.value[idx], ...data }
      }
    } catch (e: any) {
      error.value = e.message || '更新定时任务失败'
      throw e
    }
  }

  async function deleteScheduleAction(id: string) {
    try {
      await deleteSchedule(id)
      schedules.value = schedules.value.filter(s => s.id !== id)
    } catch (e: any) {
      error.value = e.message || '删除定时任务失败'
      throw e
    }
  }

  async function toggleScheduleAction(id: string, enabled: boolean) {
    const schedule = schedules.value.find(s => s.id === id)
    if (!schedule) return
    try {
      await toggleSchedule(id, enabled)
      schedule.enabled = enabled
    } catch (e: any) {
      error.value = e.message || '操作失败'
    }
  }

  return {
    schedules, loading, error, enabledSchedules,
    fetchSchedules, createScheduleAction, updateScheduleAction,
    deleteScheduleAction, toggleScheduleAction
  }
})
