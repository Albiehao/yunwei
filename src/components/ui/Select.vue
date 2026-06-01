<template>
  <div class="select-wrap" ref="wrapRef">
    <label v-if="label" class="select-label">{{ label }}</label>
    <button class="select-field" :class="{ 'select--open': open }" @click="toggle">
      <span class="select-value" :class="{ 'select-ph': !selectedLabel }">{{ selectedLabel || placeholder }}</span>
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="select-arrow"><path d="M6 9l6 6 6-6"/></svg>
    </button>
    <Transition name="drop">
      <div v-if="open" class="select-dropdown">
        <div v-for="opt in options" :key="opt.value"
          class="select-option" :class="{ 'sel--s': opt.value === modelValue }"
          @click="select(opt.value)">
          {{ opt.label }}
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
interface Opt { label: string; value: string }
const props = withDefaults(defineProps<{ modelValue: string; options: Opt[]; label?: string; placeholder?: string }>(), { label: '', placeholder: '请选择' })
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()
const open = ref(false); const wrapRef = ref<HTMLElement>()
const selectedLabel = computed(() => props.options.find(o => o.value === props.modelValue)?.label)
function toggle() { open.value = !open.value }
function select(val: string) { emit('update:modelValue', val); open.value = false }
function onClick(e: MouseEvent) { if (wrapRef.value && !wrapRef.value.contains(e.target as Node)) open.value = false }
onMounted(() => document.addEventListener('click', onClick))
onUnmounted(() => document.removeEventListener('click', onClick))
</script>

<style scoped lang="scss">
.select-wrap { position: relative; width: 100%; }
.select-label { display: block; font-size: 13px; font-weight: 500; color: var(--color-text); margin-bottom: 6px; }

.select-field {
  display: flex; align-items: center; justify-content: space-between;
  width: 100%; padding: 10px 12px;
  border: 1.5px solid var(--color-border); border-radius: var(--radius-md);
  background: var(--color-bg-card); cursor: pointer;
  font-family: var(--font-sans); font-size: 13px; text-align: left;
  color: var(--color-text); transition: all var(--transition); gap: 8px;
  &:hover { border-color: var(--color-primary-light); }
  &.select--open { border-color: var(--color-primary); box-shadow: 0 0 0 4px var(--color-primary-bg); }
}

.select-value { flex: 1; }
.select-ph { color: var(--color-text-muted); }
.select-arrow { flex-shrink: 0; color: var(--color-text-muted); transition: transform var(--transition); }
.select--open .select-arrow { transform: rotate(180deg); }

.select-dropdown {
  position: absolute; top: 100%; left: 0; right: 0; margin-top: 4px;
  background: var(--color-bg-card); border: 1px solid var(--color-border);
  border-radius: var(--radius-md); box-shadow: var(--shadow-lg);
  z-index: 100; max-height: 240px; overflow-y: auto;
}
.select-option {
  padding: 10px 12px; font-size: 13px; cursor: pointer;
  &:hover { background: var(--color-bg-hover); }
  &.sel--s { color: var(--color-primary); font-weight: 500; background: var(--color-primary-bg); }
}

.drop-enter-active, .drop-leave-active { transition: all 0.15s ease; }
.drop-enter-from, .drop-leave-to { opacity: 0; transform: translateY(-4px); }
</style>
