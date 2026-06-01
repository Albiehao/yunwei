<template>
  <div class="cron-input">
    <el-input
      :model-value="modelValue"
      @update:model-value="$emit('update:modelValue', $event)"
      placeholder="Cron 表达式 (如 0 9 * * 1-5)"
      clearable
    >
      <template #append>
        <el-tooltip :content="humanReadable">
          <el-button :icon="Clock" :disabled="!modelValue" />
        </el-tooltip>
      </template>
    </el-input>
    <p v-if="modelValue && humanReadable" class="cron-hint">
      <el-icon><InfoFilled /></el-icon> {{ humanReadable }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Clock, InfoFilled } from '@element-plus/icons-vue'

const props = defineProps<{
  modelValue: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()

// Simple cron to human readable
const humanReadable = computed(() => {
  if (!props.modelValue) return ''
  const parts = props.modelValue.trim().split(/\s+/)
  if (parts.length !== 5) return '无效的 Cron 表达式'

  const [minute, hour, dayOfMonth, month, dayOfWeek] = parts

  const dowMap = ['日', '一', '二', '三', '四', '五', '六']

  if (minute === '0' && hour !== '*') {
    const hourStr = `${hour.padStart(2, '0')}:00`
    if (dayOfWeek.startsWith('*/') ? false : dayOfWeek.match(/^[1-5](,[1-5])*$/) && dayOfMonth === '*' && month === '*') {
      const days = dayOfWeek.split(',').map(d => dowMap[parseInt(d)])
      return `每周${days.join('、')} ${hourStr} 执行`
    }
    if (dayOfWeek === '*' && dayOfMonth === '*' && month === '*') {
      return `每天 ${hourStr} 执行`
    }
    if (dayOfWeek === '0' || dayOfWeek === '6' || dayOfWeek === '0,6') {
      return `每周末 ${hourStr} 执行`
    }
    if (dayOfWeek === '1-5') {
      return `每个工作日 ${hourStr} 执行`
    }
  }

  if (minute === '0' && hour === '*' && dayOfMonth === '*' && month === '*' && dayOfWeek === '*') {
    return '每小时执行一次'
  }

  if (props.modelValue === '*/5 * * * *') return '每 5 分钟执行一次'
  if (props.modelValue === '*/10 * * * *') return '每 10 分钟执行一次'
  if (props.modelValue === '*/30 * * * *') return '每 30 分钟执行一次'

  return `Cron: ${props.modelValue}`
})
</script>

<style scoped lang="scss">
.cron-input {
  width: 100%;
}
.cron-hint {
  margin: 4px 0 0;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
