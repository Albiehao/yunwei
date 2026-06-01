<template>
  <div class="steps">
    <div
      v-for="(step, idx) in steps"
      :key="idx"
      class="step"
      :class="{
        'step--active': idx === active,
        'step--completed': idx < active,
        'step--pending': idx > active
      }"
    >
      <div class="step-indicator">
        <span v-if="idx < active" class="step-check">&#10003;</span>
        <span v-else>{{ idx + 1 }}</span>
      </div>
      <span class="step-label">{{ step }}</span>
      <div v-if="idx < steps.length - 1" class="step-line" />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  steps: string[]
  active: number
}>()
</script>

<style scoped lang="scss">
.steps {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 0;
  margin-bottom: 32px;
}

.step {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  flex: 1;
  max-width: 200px;
}

.step-indicator {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
  transition: all var(--transition);
}

.step--active .step-indicator {
  background: var(--color-primary);
  color: white;
  box-shadow: 0 0 0 4px var(--color-primary-bg);
}

.step--completed .step-indicator {
  background: var(--color-success);
  color: white;
}

.step--pending .step-indicator {
  background: var(--color-bg-hover);
  color: var(--color-text-muted);
  border: 1px solid var(--color-border);
}

.step-label {
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
}

.step--active .step-label { color: var(--color-text); font-weight: 600; }
.step--completed .step-label { color: var(--color-success); }
.step--pending .step-label { color: var(--color-text-muted); }

.step-line {
  flex: 1;
  height: 1px;
  background: var(--color-border);
  margin: 0 16px;
  margin-top: -16px;
}
.step--completed .step-line { background: var(--color-success); }
.step--active .step-line { background: var(--color-primary); }
</style>
