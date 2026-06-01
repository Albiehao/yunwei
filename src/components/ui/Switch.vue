<template>
  <button
    class="switch"
    :class="{ 'switch--on': modelValue, 'switch--off': !modelValue }"
    :disabled="disabled"
    @click="$emit('update:modelValue', !modelValue)"
  >
    <span class="switch-thumb" />
  </button>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: boolean
  disabled?: boolean
}>()

defineEmits<{
  'update:modelValue': [value: boolean]
}>()
</script>

<style scoped lang="scss">
.switch {
  position: relative;
  width: 44px;
  height: 26px;
  border-radius: 13px;
  border: none;
  cursor: pointer;
  transition: all var(--transition-smooth);
  flex-shrink: 0;
  padding: 0;

  &--on { background: var(--color-primary); }
  &--off { background: var(--color-border); }
  &:disabled { opacity: 0.5; cursor: not-allowed; }
}

.switch-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 22px;
  height: 22px;
  background: white;
  border-radius: 50%;
  transition: transform var(--transition-smooth);
  box-shadow: 0 1px 3px rgba(0,0,0,0.15), 0 1px 2px rgba(0,0,0,0.1);
}

.switch--on .switch-thumb { transform: translateX(18px); }
</style>
