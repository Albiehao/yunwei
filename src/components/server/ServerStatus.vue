<template>
  <div class="server-status" :class="`server-status--${status}`">
    <Icon :name="statusIcon" :size="16" class="status-icon" />
    <span class="status-name">{{ statusLabel }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ServerStatus } from '@/types'
import { Icon } from '@/components/ui'

const props = defineProps<{
  status: ServerStatus
}>()

const statusLabels: Record<string, string> = {
  [ServerStatus.Running]: '运行中',
  [ServerStatus.Stopped]: '已停止',
  [ServerStatus.Starting]: '启动中',
  [ServerStatus.Stopping]: '停止中',
  [ServerStatus.Pending]: '待处理',
  [ServerStatus.Error]: '异常'
}

const statusIcons: Record<string, string> = {
  [ServerStatus.Running]: 'VideoPlay',
  [ServerStatus.Stopped]: 'VideoPause',
  [ServerStatus.Starting]: 'Loading',
  [ServerStatus.Stopping]: 'Loading',
  [ServerStatus.Error]: 'WarningFilled',
  [ServerStatus.Pending]: 'InfoFilled',
}

const statusLabel = computed(() => statusLabels[props.status] || props.status)
const statusIcon = computed(() => statusIcons[props.status] || 'InfoFilled')
</script>

<style scoped lang="scss">
.server-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;

  &--running {
    color: var(--color-success);
    background: var(--color-success-bg);
    .status-icon { animation: pulse-glow 2s ease-in-out infinite; }
  }
  &--stopped {
    color: var(--color-text-muted);
    background: var(--color-bg-hover);
  }
  &--starting, &--stopping {
    color: var(--color-warning);
    background: var(--color-warning-bg);
    .status-icon { animation: spin 1s linear infinite; }
  }
  &--error {
    color: var(--color-danger);
    background: var(--color-danger-bg);
  }
  &--pending {
    color: var(--color-text-muted);
    background: var(--color-bg-hover);
  }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse-glow {
  0%, 100% { opacity: 1; filter: drop-shadow(0 0 4px rgba(22, 163, 74, 0.3)); }
  50% { opacity: 0.7; filter: drop-shadow(0 0 8px rgba(22, 163, 74, 0.5)); }
}
</style>
