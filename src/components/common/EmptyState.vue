<template>
  <div class="empty-state">
    <div class="empty-icon" v-html="iconHtml" />
    <p class="empty-text">{{ description }}</p>
    <button v-if="actionText" class="empty-btn" @click="$emit('action')">{{ actionText }}</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  type?: 'empty' | 'search'
  description?: string
  actionText?: string
}>(), {
  type: 'empty',
  description: '暂无数据'
})

defineEmits<{
  action: []
}>()

const icons = {
  empty: '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>',
  search: '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>'
}

const iconHtml = computed(() => icons[props.type])
</script>

<style scoped lang="scss">
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 16px;
}
.empty-icon {
  color: var(--color-text-muted);
  opacity: 0.5;
}
.empty-text {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
}
.empty-btn {
  padding: 8px 20px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition);
  &:hover { background: var(--color-primary-dark); }
}
</style>
