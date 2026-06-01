<template>
  <div class="server-specs">
    <div class="spec-item" v-for="spec in specList" :key="spec.label">
      <Icon :name="spec.icon" :size="14" />
      <span class="spec-value">{{ spec.value }}</span>
      <span class="spec-label">{{ spec.label }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { ServerSpec } from '@/types'
import { Icon } from '@/components/ui'

const props = defineProps<{
  spec: ServerSpec
}>()

const specList = computed(() => [
  { icon: 'Cpu', value: `${props.spec.cpu}`, label: '核' },
  { icon: 'Monitor', value: `${props.spec.memory}`, label: 'GB' },
  { icon: 'DataBoard', value: `${props.spec.disk}`, label: 'GB' },
  { icon: 'Connection', value: `${props.spec.bandwidth}`, label: 'Mbps' },
])
</script>

<style scoped lang="scss">
.server-specs {
  display: flex;
  gap: 20px;
}

.spec-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.spec-value {
  font-weight: 600;
  color: var(--color-text);
}

.spec-label {
  color: var(--color-text-muted);
}
</style>
