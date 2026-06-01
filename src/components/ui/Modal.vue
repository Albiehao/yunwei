<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="open" class="modal-overlay" @click.self="handleOverlayClick">
        <div class="modal" :style="{ maxWidth: width }">
          <div class="modal-header">
            <div>
              <h3 class="modal-title">{{ title }}</h3>
              <p v-if="subtitle" class="modal-subtitle">{{ subtitle }}</p>
            </div>
            <button class="modal-close" @click="close">
              <Icon name="close" :size="18" />
            </button>
          </div>
          <div class="modal-body"><slot /></div>
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import Icon from './Icon.vue'

const props = withDefaults(defineProps<{
  open: boolean
  title?: string
  subtitle?: string
  width?: string
  closable?: boolean
}>(), { title: '', subtitle: '', width: '480px', closable: true })

const emit = defineEmits<{ 'update:open': [value: boolean]; close: [] }>()
function close() { emit('update:open', false); emit('close') }
function handleOverlayClick() { if (props.closable) close() }
</script>

<style scoped lang="scss">
.modal-overlay {
  position: fixed; inset: 0;
  background: var(--color-bg-overlay);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000; padding: 20px;
  backdrop-filter: blur(8px);
}

.modal {
  background: var(--glass-card);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid var(--glass-card-border);
  border-radius: var(--radius-2xl);
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
}

.modal-header {
  display: flex; align-items: flex-start; justify-content: space-between;
  padding: 24px 28px 0;
  gap: 16px;
}
.modal-title { font-size: 18px; font-weight: 700; margin: 0; }
.modal-subtitle { font-size: 13px; color: var(--color-text-secondary); margin: 4px 0 0; }
.modal-close {
  width: 32px; height: 32px; display: flex; align-items: center; justify-content: center;
  border: none; background: transparent; border-radius: var(--radius-full);
  cursor: pointer; color: var(--color-text-muted); flex-shrink: 0;
  transition: all var(--transition);
  &:hover { background: var(--color-bg-hover); color: var(--color-text); }
}
.modal-body { padding: 24px 28px; }
.modal-footer {
  display: flex; justify-content: flex-end; gap: 8px;
  padding: 16px 28px 24px;
  border-top: 1px solid var(--color-border-light);
}

.modal-enter-active, .modal-leave-active { transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1); }
.modal-enter-from, .modal-leave-to { opacity: 0; .modal { transform: scale(0.92) translateY(12px); } }
</style>
