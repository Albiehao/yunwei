<template>
  <el-dialog
    v-model="visible"
    :title="isEdit ? '编辑定时任务' : '新建定时任务'"
    width="560px"
    :close-on-click-modal="false"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      label-position="right"
    >
      <el-form-item label="任务名称" prop="name">
        <el-input v-model="form.name" placeholder="给定时任务起个名字" />
      </el-form-item>
      <el-form-item label="目标服务器" prop="serverId">
        <el-select v-model="form.serverId" placeholder="选择服务器" style="width:100%">
          <el-option
            v-for="s in servers"
            :key="s.id"
            :label="s.name"
            :value="s.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="执行动作" prop="action">
        <el-radio-group v-model="form.action">
          <el-radio-button value="start">开机</el-radio-button>
          <el-radio-button value="stop">关机</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="Cron 表达式" prop="cronExpression">
        <CronInput v-model="form.cronExpression" />
      </el-form-item>
      <el-form-item label="时区" prop="timezone">
        <el-select v-model="form.timezone" style="width:100%">
          <el-option label="Asia/Shanghai (UTC+8)" value="Asia/Shanghai" />
          <el-option label="UTC" value="UTC" />
          <el-option label="America/New_York" value="America/New_York" />
        </el-select>
      </el-form-item>
      <el-form-item label="立即启用">
        <el-switch v-model="form.enabled" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleSubmit">
        {{ isEdit ? '保存' : '创建' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import type { Schedule, ScheduleFormData } from '@/types'
import { ScheduleAction } from '@/types'
import CronInput from './CronInput.vue'
import type { Server } from '@/types'

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

const visible = ref(props.modelValue)
const isEdit = ref(!!props.schedule)
const submitting = ref(false)
const formRef = ref()

const form = reactive<ScheduleFormData>({
  name: '',
  serverId: '',
  action: ScheduleAction.Start,
  cronExpression: '0 9 * * 1-5',
  timezone: 'Asia/Shanghai',
  enabled: true
})

const rules = {
  name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  serverId: [{ required: true, message: '请选择目标服务器', trigger: 'change' }],
  action: [{ required: true, message: '请选择执行动作', trigger: 'change' }],
  cronExpression: [{ required: true, message: '请输入 Cron 表达式', trigger: 'blur' }],
  timezone: [{ required: true, message: '请选择时区', trigger: 'change' }]
}

watch(() => props.modelValue, (val) => {
  visible.value = val
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

watch(visible, (val) => {
  emit('update:modelValue', val)
})

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  submitting.value = true
  emit('submit', { ...form })
  submitting.value = false
  visible.value = false
}
</script>
