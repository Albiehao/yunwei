<template>
  <div class="server-controls">
    <Button
      v-if="status === ServerStatus.Stopped || status === ServerStatus.Error"
      variant="success"
      size="sm"
      :loading="status === ServerStatus.Starting"
      :disabled="status === ServerStatus.Starting"
      @click="$emit('start')"
    >
      启动
    </Button>
    <Button
      v-if="status === ServerStatus.Running"
      variant="danger"
      size="sm"
      :loading="status === ServerStatus.Stopping"
      :disabled="status === ServerStatus.Stopping"
      @click="$emit('stop')"
    >
      停止
    </Button>
    <Badge
      v-if="status === ServerStatus.Starting"
      variant="warning"
    >
      启动中...
    </Badge>
    <Badge
      v-if="status === ServerStatus.Stopping"
      variant="warning"
    >
      停止中...
    </Badge>
  </div>
</template>

<script setup lang="ts">
import { ServerStatus } from '@/types'
import { Button, Badge } from '@/components/ui'

defineProps<{
  status: ServerStatus
}>()

defineEmits<{
  start: []
  stop: []
}>()
</script>

<style scoped lang="scss">
.server-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>
