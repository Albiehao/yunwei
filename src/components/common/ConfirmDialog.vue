<template>
  <el-dialog
    v-model="visible"
    :title="title"
    :width="width"
    :close-on-click-modal="false"
    :before-close="handleCancel"
  >
    <div class="confirm-body">
      <el-icon :size="24" :color="iconColor" class="confirm-icon">
        <WarningFilled v-if="type === 'warning'" />
        <InfoFilled v-else-if="type === 'info'" />
        <CircleCloseFilled v-else-if="type === 'danger'" />
        <SuccessFilled v-else />
      </el-icon>
      <p class="confirm-message">{{ message }}</p>
    </div>
    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button
        :type="type === 'danger' ? 'danger' : 'primary'"
        :loading="loading"
        @click="handleConfirm"
      >
        {{ confirmText }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = withDefaults(defineProps<{
  modelValue: boolean
  title?: string
  message: string
  type?: 'info' | 'warning' | 'danger'
  confirmText?: string
  width?: string
  loading?: boolean
}>(), {
  title: '确认操作',
  type: 'warning',
  confirmText: '确认',
  width: '420px',
  loading: false
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'confirm': []
  'cancel': []
}>()

const visible = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

const iconColor = {
  info: 'var(--el-color-primary)',
  warning: 'var(--el-color-warning)',
  danger: 'var(--el-color-danger)'
}[props.type]

function handleConfirm() {
  emit('confirm')
}

function handleCancel() {
  emit('cancel')
}
</script>

<style scoped lang="scss">
.confirm-body {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 8px 0;
}
.confirm-icon {
  flex-shrink: 0;
  margin-top: 2px;
}
.confirm-message {
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-primary);
  margin: 0;
}
</style>
