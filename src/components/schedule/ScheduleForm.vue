<template>
  <Modal :open="modelValue" :title="isEdit ? '编辑定时任务' : '新建定时任务'" width="560px" @update:open="$emit('update:modelValue', $event)">
    <div class="schedule-form">
      <div class="form-item">
        <label class="form-label">任务名称</label>
        <Input v-model="form.name" placeholder="给定时任务起个名字" />
      </div>
      <div class="form-item">
        <label class="form-label">目标服务器</label>
        <Select v-model="form.serverId" :options="serverOptions" placeholder="选择服务器" />
      </div>
      <div class="form-item">
        <label class="form-label">执行动作</label>
        <div class="radio-group">
          <label class="radio-btn" :class="{ 'radio-btn--active': form.action === 'start' }">
            <input type="radio" value="start" v-model="form.action" class="radio-input" />
            开机
          </label>
          <label class="radio-btn" :class="{ 'radio-btn--active': form.action === 'stop' }">
            <input type="radio" value="stop" v-model="form.action" class="radio-input" />
            关机
          </label>
        </div>
      </div>
      <CronInput v-model="form.cronExpression" />
      <div class="form-item">
        <label class="form-label">立即启用</label>
        <Switch v-model="form.enabled" />
      </div>
    </div>
    <template #footer>
      <Button variant="secondary" @click="$emit('update:modelValue', false)">取消</Button>
      <Button variant="primary" :loading="submitting" @click="handleSubmit">
        {{ isEdit ? '保存' : '创建' }}
      </Button>
    </template>
  </Modal>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import type { Schedule, ScheduleFormData } from '@/types'
import { ScheduleAction } from '@/types'
import CronInput from './CronInput.vue'
import type { Server } from '@/types'
import { Modal, Button, Input, Select, Switch } from '@/components/ui'

const props = withDefaults(defineProps<{
  modelValue: boolean
  schedule?: Schedule | null
  servers: Server[]
}>(), {
  modelValue: false,
  schedule: null
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  submit: [data: ScheduleFormData]
}>()

const isEdit = ref(!!props.schedule)
const submitting = ref(false)

const form = reactive<ScheduleFormData>({
  name: '',
  serverId: '',
  action: ScheduleAction.Start,
  cronExpression: '0 9 * * 1-5',
  timezone: 'Asia/Shanghai',
  enabled: true
})

const serverOptions = computed(() =>
  props.servers.map(s => ({ label: s.name, value: s.id }))
)

watch(() => props.modelValue, (val) => {
  if (val && props.schedule) {
    isEdit.value = true
    Object.assign(form, {
      name: props.schedule.name,
      serverId: props.schedule.serverId,
      action: props.schedule.action,
      cronExpression: props.schedule.cronExpression,
      timezone: props.schedule.timezone,
      enabled: props.schedule.enabled
    })
  } else if (val && !props.schedule) {
    isEdit.value = false
    Object.assign(form, {
      name: '', serverId: '', action: ScheduleAction.Start,
      cronExpression: '0 9 * * 1-5', timezone: 'Asia/Shanghai', enabled: true
    })
  }
})

async function handleSubmit() {
  submitting.value = true
  emit('submit', { ...form })
  submitting.value = false
}
</script>

<style scoped lang="scss">
.schedule-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-item {
  .form-label {
    display: block;
    font-size: 13px;
    font-weight: 500;
    color: var(--color-text);
    margin-bottom: 6px;
  }
}

.radio-group {
  display: flex;
  gap: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  width: fit-content;
}

.radio-btn {
  padding: 9px 20px;
  font-size: 13px;
  cursor: pointer;
  transition: all var(--transition);
  border-right: 1px solid var(--color-border);

  &:last-child { border-right: none; }

  .radio-input {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
  }

  &--active {
    background: var(--color-primary);
    color: white;
  }

  &:not(.radio-btn--active):hover {
    background: var(--color-bg-hover);
  }
}
</style>
