<template>
  <label class="checkbox">
    <input
      type="radio"
      class="checkbox-input"
      :checked="modelValue === value"
      :name="name"
      :value="value"
      @change="$emit('update:modelValue', value)"
    />
    <span class="checkbox-indicator" />
    <span class="checkbox-label"><slot /></span>
  </label>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
  value: string
  name?: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<style scoped lang="scss">
.checkbox {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.checkbox-indicator {
  width: 16px;
  height: 16px;
  border: 2px solid var(--color-border);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
  flex-shrink: 0;
}

.checkbox-input:checked + .checkbox-indicator {
  border-color: var(--color-primary);
  background: var(--color-primary);
  box-shadow: inset 0 0 0 3px white;
}

.checkbox-label { font-size: 13px; }
</style>
