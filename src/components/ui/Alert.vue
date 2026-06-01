<template>
  <Transition name="al">
    <div v-if="visible" class="alert" :class="`alert--${type}`">
      <Icon :name="iconName" :size="18" class="alert-icon" />
      <span class="alert-text"><slot /></span>
      <button v-if="closable" class="alert-close" @click="visible = false">
        <Icon name="close" :size="14" />
      </button>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Icon from './Icon.vue'

const props = withDefaults(defineProps<{ type?: 'info' | 'success' | 'warning' | 'danger'; closable?: boolean }>(), { type: 'info', closable: true })
const visible = ref(true)
const iconName = computed(() => ({ info: 'info', success: 'check', warning: 'warning', danger: 'close-circle' }[props.type]))
</script>

<style scoped lang="scss">
.alert {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 14px 16px; border-radius: var(--radius-lg);
  font-size: 13px; line-height: 1.5;
  border: 1px solid transparent;
}
.alert-icon { flex-shrink: 0; margin-top: 1px; }
.alert-text { flex: 1; }
.alert-close { flex-shrink: 0; background: none; border: none; cursor: pointer; opacity: 0.5; color: inherit; padding: 0; &:hover { opacity: 1; } }

.alert--info { background: var(--color-primary-bg); color: var(--color-primary); border-color: rgba(99,102,241,0.15); }
.alert--success { background: var(--color-success-bg); color: var(--color-success); border-color: rgba(16,185,129,0.15); }
.alert--warning { background: var(--color-warning-bg); color: var(--color-warning); border-color: rgba(245,158,11,0.15); }
.alert--danger { background: var(--color-danger-bg); color: var(--color-danger); border-color: rgba(239,68,68,0.15); }

.al-enter-active, .al-leave-active { transition: all 0.2s; }
.al-enter-from, .al-leave-to { opacity: 0; transform: translateY(-8px); }
</style>
