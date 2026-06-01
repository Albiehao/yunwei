<template>
  <div class="server-controls">
    <!-- Running -->
    <template v-if="status === 'running'">
      <template v-if="chargeType === 'PostPaid'">
        <Button variant="warning" size="sm" :loading="stoppingFree" :disabled="stoppingFree" @click="$emit('stop', 'StopCharging')">
          停止不收费
        </Button>
        <Button variant="danger" size="sm" :loading="stoppingPaid" :disabled="stoppingPaid" @click="$emit('stop', 'KeepCharging')">
          停止计费
        </Button>
      </template>
      <Button v-else variant="danger" size="sm" :loading="stoppingPaid" @click="$emit('stop', 'KeepCharging')">
        停止
      </Button>
    </template>

    <!-- Stopped / Error -->
    <template v-if="status === 'stopped' || status === 'error'">
      <Button variant="success" size="sm" :loading="(status as string) === 'starting'" :disabled="(status as string) === 'starting'" @click="$emit('start')">
        启动
      </Button>
    </template>

    <!-- Transient states -->
    <Badge v-if="(status as string) === 'starting'" variant="warning">启动中...</Badge>
    <Badge v-if="status === 'stopping'" variant="warning">停止中...</Badge>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Button, Badge } from '@/components/ui'
const stoppingFree = ref(false)
const stoppingPaid = ref(false)

defineProps<{
  status: string
  chargeType?: string
}>()

defineEmits<{
  start: []
  stop: [mode: string]
  release: []
}>()
</script>

<style scoped lang="scss">
.server-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>
