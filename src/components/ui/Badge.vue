<template>
  <span class="badge" :class="`badge--${variant}`">
    <span v-if="dot" class="badge-dot" :class="`dot--${variant}`" />
    <slot />
  </span>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'danger' | 'info'
  dot?: boolean
}>(), { variant: 'default', dot: false })
</script>

<style scoped lang="scss">
.badge {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 3px 10px; border-radius: var(--radius-full);
  font-size: 12px; font-weight: 600; white-space: nowrap;
  letter-spacing: 0.2px;
}

.badge-dot { width: 6px; height: 6px; border-radius: 50%; }

.badge--default { background: var(--color-bg-hover); color: var(--color-text-secondary); }
.badge--primary { background: var(--color-primary-bg); color: var(--color-primary); }
.badge--success { background: var(--color-success-bg); color: var(--color-success); }
.badge--warning { background: var(--color-warning-bg); color: var(--color-warning); }
.badge--danger { background: var(--color-danger-bg); color: var(--color-danger); }
.badge--info { background: var(--color-bg-hover); color: var(--color-text-secondary); }

.dot--primary { background: var(--color-primary); }
.dot--success { background: var(--color-success); box-shadow: 0 0 6px rgba(16,185,129,0.5); }
.dot--warning { background: var(--color-warning); }
.dot--danger { background: var(--color-danger); }
</style>
