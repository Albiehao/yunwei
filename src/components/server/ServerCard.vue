<template>
  <div class="server-card">
    <div class="server-card-header">
      <div class="server-info">
        <h3 class="server-name">{{ server.name }}</h3>
        <ServerStatus :status="server.status" />
      </div>
      <ServerControls
        :status="server.status"
        @start="$emit('start', server.id)"
        @stop="handleStop"
      />
    </div>
    <div class="server-card-body">
      <div class="server-meta">
        <span class="meta-item">
          <Icon name="Iphone" :size="14" />
          {{ server.instanceType }}
        </span>
        <span class="meta-item">
          <Icon name="Location" :size="14" />
          {{ server.region }}
        </span>
        <span class="meta-item">
          <Icon name="Link" :size="14" />
          {{ server.ipAddress }}
        </span>
        <span class="meta-item">
          <Icon name="Coin" :size="14" />
          {{ server.chargeType === 'PostPaid' ? '按量付费' : '包年包月' }}
        </span>
      </div>
      <hr class="divider" />
      <ServerSpecs :spec="server.spec" />
    </div>
    <ConfirmDialog
      v-model:modelValue="stopDialogVisible"
      title="停止服务器"
      :message="`确定要停止服务器「${server.name}」吗？停止后将无法访问。`"
      type="danger"
      confirmText="确认停止"
      @confirm="handleStopConfirm"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Server } from '@/types'
import ServerStatus from './ServerStatus.vue'
import ServerControls from './ServerControls.vue'
import ServerSpecs from './ServerSpecs.vue'
import { ConfirmDialog } from '@/components/common'
import { Icon } from '@/components/ui'

const props = defineProps<{
  server: Server
}>()

const emit = defineEmits<{
  start: [id: string]
  stop: [id: string]
}>()

const stopDialogVisible = ref(false)
let pendingStopId = ''

function handleStop() {
  pendingStopId = props.server.id
  stopDialogVisible.value = true
}

function handleStopConfirm() {
  stopDialogVisible.value = false
  emit('stop', pendingStopId)
}
</script>

<style scoped lang="scss">
.server-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 16px;
  transition: all var(--transition);
  animation: card-enter 0.35s ease both;
  animation-delay: calc(var(--i, 0) * 0.06s);

  &:hover {
    box-shadow: var(--shadow-sm);
  }
}

@keyframes card-enter {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.server-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.server-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.server-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.server-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 4px;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.divider {
  border: none;
  border-top: 1px solid var(--color-border-light);
  margin: 12px 0;
}
</style>
