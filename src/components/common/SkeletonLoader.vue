<template>
  <div class="skeleton" :style="{ height }">
    <div v-for="i in count" :key="i" class="skeleton-item" />
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  count?: number
  height?: string
}>(), {
  count: 3,
  height: '100%'
})
</script>

<style scoped lang="scss">
.skeleton {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px 0;
}
.skeleton-item {
  height: 16px;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--color-border-light) 25%, var(--color-border) 50%, var(--color-border-light) 75%);
  background-size: 200% 100%;
  animation: sk-shimmer 1.5s infinite;
  &:nth-child(2) { width: 85%; }
  &:nth-child(3) { width: 70%; }
}
@keyframes sk-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
