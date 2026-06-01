<template>
  <div class="input-wrap">
    <label v-if="label" class="input-label">{{ label }}</label>
    <div class="input-field" :class="{ 'input--error': error, 'input--focused': focused }">
      <Icon v-if="prefixIcon" :name="prefixIcon" :size="16" class="input-prefix" />
      <input
        :type="type" :value="modelValue" :placeholder="placeholder" :disabled="disabled"
        class="input-control"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        @focus="focused = true; $emit('focus')"
        @blur="focused = false; $emit('blur')"
      />
    </div>
    <p v-if="error" class="input-error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Icon from './Icon.vue'

withDefaults(defineProps<{
  modelValue: string | number; label?: string; placeholder?: string
  type?: string; disabled?: boolean; error?: string; prefixIcon?: string
}>(), { label: '', placeholder: '', type: 'text', disabled: false, error: '', prefixIcon: '' })

defineEmits<{ 'update:modelValue': [value: string]; focus: []; blur: [] }>()
const focused = ref(false)
</script>

<style scoped lang="scss">
.input-wrap { width: 100%; }
.input-label { display: block; font-size: 13px; font-weight: 500; color: var(--color-text); margin-bottom: 6px; }

.input-field {
  display: flex; align-items: center;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-bg-card);
  transition: all var(--transition);
  overflow: hidden;

  &:focus-within, &.input--focused {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 4px var(--color-primary-bg);
  }
  &.input--error { border-color: var(--color-danger);
    &:focus-within { box-shadow: 0 0 0 4px var(--color-danger-bg); }
  }
}

.input-prefix { display: flex; align-items: center; padding-left: 12px; color: var(--color-text-muted); }

.input-control {
  width: 100%; padding: 10px 12px;
  border: none; outline: none; background: transparent;
  font-family: var(--font-sans); font-size: 13px; color: var(--color-text);
  &::placeholder { color: var(--color-text-muted); }
}

.input-error { font-size: 12px; color: var(--color-danger); margin-top: 4px; }
</style>
