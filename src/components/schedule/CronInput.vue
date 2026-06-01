<template>
  <div class="cron-input">
    <div class="cron-row">
      <label class="cron-label">频率</label>
      <Select v-model="frequency" :options="freqOptions" />
    </div>
    <div class="cron-row">
      <label class="cron-label">时间</label>
      <div class="cron-time">
        <Select v-model="hour" :options="hourOptions" />
        <span class="cron-colon">:</span>
        <Select v-model="minute" :options="minuteOptions" />
      </div>
    </div>
    <div v-if="frequency === 'interval'" class="cron-row">
      <label class="cron-label">间隔</label>
      <Select v-model="intervalMin" :options="intervalOptions" />
    </div>
    <div v-if="frequency === 'custom'" class="cron-row">
      <label class="cron-label">星期</label>
      <div class="cron-days">
        <label v-for="d in dayOptions" :key="d.value"
          class="day-btn" :class="{ 'day-btn--on': selectedDays.includes(d.value) }">
          <input type="checkbox" :value="d.value" v-model="selectedDays" class="day-input" />
          {{ d.label }}
        </label>
      </div>
    </div>
    <p class="cron-preview">
      <Icon name="schedule" :size="14" />
      {{ previewText }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Select, Icon } from '@/components/ui'

const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

// Parse incoming cron to form state
const frequency = ref('workday')
const hour = ref('9')
const minute = ref('0')
const intervalMin = ref('5')
const intervalOptions = [
  { label: '5 分钟', value: '5' },
  { label: '10 分钟', value: '10' },
  { label: '15 分钟', value: '15' },
  { label: '30 分钟', value: '30' },
]
const selectedDays = ref<string[]>(['1', '2', '3', '4', '5'])

const freqOptions = [
  { label: '每天', value: 'daily' },
  { label: '工作日（周一至周五）', value: 'workday' },
  { label: '每N分钟', value: 'interval' },
  { label: '自定义星期', value: 'custom' },
]

const hourOptions = Array.from({ length: 24 }, (_, i) => ({
  label: `${String(i).padStart(2, '0')} 时`, value: String(i)
}))

const minuteOptions = Array.from({ length: 60 }, (_, i) => ({
  label: `${String(i).padStart(2, '0')} 分`, value: String(i)
}))

const dayOptions = [
  { label: '一', value: '1' },
  { label: '二', value: '2' },
  { label: '三', value: '3' },
  { label: '四', value: '4' },
  { label: '五', value: '5' },
  { label: '六', value: '6' },
  { label: '日', value: '0' },
]

const dayLabels: Record<string, string> = { '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '0': '日' }

// Generate cron expression from form
function generateCron(): string {
  const h = hour.value
  const m = minute.value
  if (frequency.value === 'daily') return `${m} ${h} * * *`
  if (frequency.value === 'workday') return `${m} ${h} * * 1-5`
  if (frequency.value === 'interval') return `*/${intervalMin.value} * * * *`
  if (frequency.value === 'custom') {
    if (selectedDays.value.length === 0) return `${m} ${h} * * *`
    return `${m} ${h} * * ${selectedDays.value.sort().join(',')}`
  }
  return props.modelValue
}

// Preview text
const previewText = computed(() => {
  const h = hour.value.padStart(2, '0')
  const m = minute.value.padStart(2, '0')
  const time = `${h}:${m}`
  if (frequency.value === 'daily') return `每天 ${time} 执行`
  if (frequency.value === 'workday') return `周一至周五 ${time} 执行`
  if (frequency.value === 'interval') return `每 ${intervalMin.value} 分钟执行一次`
  if (frequency.value === 'custom') {
    if (selectedDays.value.length === 0) return `请选择至少一天`
    const days = selectedDays.value.sort().map(d => dayLabels[d]).join('、')
    return `每周${days} ${time} 执行`
  }
  return ''
})

// Sync to parent
watch([frequency, hour, minute, intervalMin, selectedDays], () => {
  emit('update:modelValue', generateCron())
}, { immediate: true })

// Parse initial value
watch(() => props.modelValue, (val) => {
  if (!val) return
  const parts = val.trim().split(/\s+/)
  if (parts.length !== 5) return
  const [m, h, , , dow] = parts
  minute.value = m === '*' ? '0' : m
  hour.value = h === '*' ? '9' : h
  if (m.startsWith('*/')) {
    frequency.value = 'interval'
    intervalMin.value = m.slice(2)
  } else if (dow === '*' || dow === '?') {
    frequency.value = 'daily'
  } else if (dow === '1-5') {
    frequency.value = 'workday'
  } else {
    frequency.value = 'custom'
    selectedDays.value = dow.split(',').sort()
  }
}, { immediate: false })
</script>

<style scoped lang="scss">
.cron-input {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.cron-row {
  display: flex;
  align-items: center;
  gap: 12px;
}
.cron-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  min-width: 40px;
  flex-shrink: 0;
}
.cron-time {
  display: flex;
  align-items: center;
  gap: 4px;
}
.cron-colon {
  font-weight: 700;
  font-size: 16px;
  color: var(--color-text);
}
.cron-days {
  display: flex;
  gap: 6px;
}
.day-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition);
  color: var(--color-text-secondary);
  background: var(--color-bg-card);
  &:hover { border-color: var(--color-primary-light); }
}
.day-input { position: absolute; opacity: 0; width: 0; height: 0; }
.day-btn--on {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}
.cron-preview {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-primary);
  font-weight: 500;
  margin: 0;
  padding: 8px 12px;
  background: var(--color-primary-bg);
  border-radius: var(--radius-sm);
}
</style>
