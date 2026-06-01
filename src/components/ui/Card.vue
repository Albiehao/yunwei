<template>
  <div class="card" :class="{ 'card--hover': hoverable }">
    <div v-if="$slots.header || title" class="card-header">
      <h3 v-if="title" class="card-title">{{ title }}</h3>
      <slot name="header" />
      <div v-if="$slots.actions" class="card-actions"><slot name="actions" /></div>
    </div>
    <div class="card-body"><slot /></div>
    <div v-if="$slots.footer" class="card-footer"><slot name="footer" /></div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title?: string
  hoverable?: boolean
}>(), { title: '', hoverable: false })
</script>

<style scoped lang="scss">
.card {
  background: var(--glass-card);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-card-border);
  border-radius: var(--radius-xl);
  transition: all var(--transition-smooth);

  &--hover:hover {
    box-shadow: var(--shadow-glass);
    transform: translateY(-2px);
    border-color: var(--color-primary-light);
  }
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 22px;
  border-bottom: 1px solid var(--color-border-light);
  gap: 12px;
}

.card-title { font-size: 15px; font-weight: 600; margin: 0; }
.card-actions { display: flex; gap: 8px; flex-shrink: 0; }
.card-body { padding: 0 22px 22px; }
.card-header + .card-body { padding-top: 18px; }

.card-footer {
  padding: 14px 22px;
  border-top: 1px solid var(--color-border-light);
  font-size: 13px;
  color: var(--color-text-secondary);
}
</style>
