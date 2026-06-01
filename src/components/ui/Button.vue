<template>
  <button
    class="btn"
    :class="[`btn--${variant}`, `btn--${size}`, { 'btn--loading': loading }]"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="btn-spinner" />
    <Icon v-else-if="icon" :name="icon" :size="size === 'sm' ? 14 : size === 'lg' ? 18 : 16" />
    <span v-if="$slots.default" class="btn-text"><slot /></span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Icon from './Icon.vue'

const props = withDefaults(defineProps<{
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
  icon?: string
}>(), { variant: 'primary', size: 'md', loading: false, disabled: false, icon: '' })

defineEmits<{ click: [e: MouseEvent] }>()
</script>

<style scoped lang="scss">
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border: none;
  border-radius: var(--radius-full);
  font-family: var(--font-sans);
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition);
  white-space: nowrap;
  outline: none;
  line-height: 1;

  &:disabled { opacity: 0.4; cursor: not-allowed; }
  &:focus-visible { box-shadow: 0 0 0 3px var(--color-primary-bg); }

  &--sm { padding: 6px 14px; font-size: 12px; }
  &--md { padding: 8px 18px; }
  &--lg { padding: 12px 24px; font-size: 15px; }

  &--primary {
    background: var(--color-primary); color: white;
    &:hover:not(:disabled) { background: var(--color-primary-hover); transform: scale(1.02); }
    &:active:not(:disabled) { transform: scale(0.98); }
  }
  &--secondary {
    background: var(--glass-card); color: var(--color-text);
    border: 1px solid var(--color-border);
    &:hover:not(:disabled) { background: var(--color-bg-hover); }
  }
  &--success { background: var(--color-success); color: white;
    &:hover:not(:disabled) { filter: brightness(0.95); transform: scale(1.02); }
  }
  &--danger { background: var(--color-danger); color: white;
    &:hover:not(:disabled) { filter: brightness(0.95); transform: scale(1.02); }
  }
  &--ghost { background: transparent; color: var(--color-text-secondary);
    &:hover:not(:disabled) { background: var(--color-bg-hover); color: var(--color-primary); }
  }
}

.btn-spinner {
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>
