<template>
  <span class="status-badge" :class="`status--${statusClass}`">
    <span class="status-dot" />
    <span class="status-text">{{ label }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: 'running' | 'stopped' | 'starting' | 'stopping' | 'pending' | 'error' | 'enabled' | 'disabled'
}>()

const statusMap: Record<string, { cls: string; label: string }> = {
  running:  { cls: 'success', label: '运行中' },
  stopped:  { cls: 'default', label: '已停止' },
  starting: { cls: 'warning', label: '启动中' },
  stopping: { cls: 'warning', label: '停止中' },
  pending:  { cls: 'default', label: '待处理' },
  error:    { cls: 'danger', label: '异常' },
  enabled:  { cls: 'success', label: '已启用' },
  disabled: { cls: 'default', label: '已停用' },
}

const statusClass = computed(() => statusMap[props.status]?.cls || '')
const label = computed(() => statusMap[props.status]?.label || props.status)
</script>

<style scoped lang="scss">
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status--success .status-dot { background: var(--color-success); box-shadow: 0 0 6px rgba(16,185,129,0.4); }
.status--default .status-dot { background: var(--color-text-muted); }
.status--warning .status-dot {
  background: var(--color-warning);
  animation: pulse 1.2s infinite;
}
.status--danger .status-dot {
  background: var(--color-danger);
  animation: pulse 0.8s infinite;
}
.status--success .status-text { color: var(--color-success); }
.status--default .status-text { color: var(--color-text-secondary); }
.status--warning .status-text { color: var(--color-warning); }
.status--danger .status-text { color: var(--color-danger); }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>
