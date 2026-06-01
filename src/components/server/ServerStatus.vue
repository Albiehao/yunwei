<template>
  <div class="server-status" :class="`server-status--${status}`">
    <el-icon :size="16" class="status-icon">
      <VideoPlay v-if="status === 'running'" />
      <VideoPause v-else-if="status === 'stopped'" />
      <Loading v-else-if="status === 'starting' || status === 'stopping'" />
      <WarningFilled v-else />
    </el-icon>
    <span class="status-name">{{ statusLabel }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ServerStatus } from '@/types'

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

const statusLabel = computed(() => statusLabels[props.status] || props.status)
</script>

<style scoped lang="scss">
.server-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;

  &--running {
    color: #67c23a;
    background: rgba(103, 194, 58, 0.1);
  }
  &--stopped {
    color: #909399;
    background: rgba(144, 147, 153, 0.1);
  }
  &--starting, &--stopping {
    color: #e6a23c;
    background: rgba(230, 162, 60, 0.1);
    .status-icon { animation: spin 1s linear infinite; }
  }
  &--error {
    color: #f56c6c;
    background: rgba(245, 108, 108, 0.1);
  }
  &--pending {
    color: #909399;
    background: rgba(144, 147, 153, 0.1);
  }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
