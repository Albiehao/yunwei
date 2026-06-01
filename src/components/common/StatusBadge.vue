<template>
  <span class="status-badge" :class="statusClass">
    <span class="status-dot" />
    <span class="status-label">{{ label }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  status: 'running' | 'stopped' | 'starting' | 'stopping' | 'pending' | 'error' | 'enabled' | 'disabled'
}>()

const statusMap: Record<string, { class: string; label: string }> = {
  running:  { class: 'status-running', label: '运行中' },
  stopped:  { class: 'status-stopped', label: '已停止' },
  starting: { class: 'status-starting', label: '启动中' },
  stopping: { class: 'status-stopping', label: '停止中' },
  pending:  { class: 'status-pending', label: '待处理' },
  error:    { class: 'status-error', label: '异常' },
  enabled:  { class: 'status-running', label: '已启用' },
  disabled: { class: 'status-stopped', label: '已停用' },
}

const statusClass = computed(() => statusMap[props.status]?.class || '')
const label = computed(() => statusMap[props.status]?.label || props.status)
</script>

<style scoped lang="scss">
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-running .status-dot {
  background-color: #67c23a;
  box-shadow: 0 0 6px rgba(103, 194, 58, 0.4);
}
.status-stopped .status-dot {
  background-color: #909399;
}
.status-starting .status-dot {
  background-color: #e6a23c;
  animation: pulse 1.2s infinite;
}
.status-stopping .status-dot {
  background-color: #f56c6c;
  animation: pulse 1.2s infinite;
}
.status-pending .status-dot {
  background-color: #909399;
}
.status-error .status-dot {
  background-color: #f56c6c;
  animation: pulse 0.8s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>
