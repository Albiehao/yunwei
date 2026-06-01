import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { PayAsYouGoService } from '@/types'
import { getServices, updateService } from '@/api/service'

export const useServiceStore = defineStore('service', () => {
  const services = ref<PayAsYouGoService[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const activeServices = computed(() => services.value.filter(s => s.enabled))
  const totalMonthlyCost = computed(() =>
    services.value.reduce((sum, s) => sum + (s.enabled ? s.monthlyCost : 0), 0)
  )

  async function fetchServices() {
    loading.value = true
    error.value = null
    try {
      const res = await getServices()
      services.value = res.data
    } catch (e: any) {
      error.value = e.message || '获取服务列表失败'
    } finally {
      loading.value = false
    }
  }

  async function toggleService(id: string, enabled: boolean) {
    const service = services.value.find(s => s.id === id)
    if (!service) return
    try {
      await updateService(id, { enabled })
      service.enabled = enabled
    } catch (e: any) {
      error.value = e.message || '操作失败'
    }
  }

  return {
    services, loading, error,
    activeServices, totalMonthlyCost,
    fetchServices, toggleService
  }
})
