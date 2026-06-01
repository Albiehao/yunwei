<template>
  <Modal :open="modelValue" :title="title" width="400px" @update:open="$emit('update:modelValue', $event)">
    <div class="confirm-body">
      <p class="confirm-message">{{ message }}</p>
    </div>
    <template #footer>
      <button class="btn btn--secondary" @click="$emit('update:modelValue', false)">取消</button>
      <button class="btn" :class="`btn--${type === 'danger' ? 'danger' : 'primary'}`" :disabled="loading" @click="$emit('confirm')">
        {{ loading ? '处理中...' : confirmText }}
      </button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '@/components/ui/Modal.vue'

withDefaults(defineProps<{
  modelValue: boolean
  title?: string
  message: string
  type?: 'info' | 'warning' | 'danger'
  confirmText?: string
  loading?: boolean
}>(), {
  title: '确认操作',
  type: 'warning',
  confirmText: '确认',
  loading: false
})

defineEmits<{
  'update:modelValue': [value: boolean]
  confirm: []
}>()
</script>

<style scoped lang="scss">
.confirm-body { padding: 8px 0; }
.confirm-message {
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text);
  margin: 0;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  font-family: var(--font-sans);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition);

  &--primary { background: var(--color-primary); color: white; &:hover { background: var(--color-primary-dark); } }
  &--secondary { background: var(--color-bg-card); color: var(--color-text); border-color: var(--color-border); &:hover { background: var(--color-bg-hover); } }
  &--danger { background: var(--color-danger); color: white; &:hover { filter: brightness(0.9); } }
  &:disabled { opacity: 0.5; cursor: not-allowed; }
}
</style>
