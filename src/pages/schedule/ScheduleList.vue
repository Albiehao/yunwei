<template>
  <div class="schedule-list-page">
    <PageHeader title="定时任务" description="设置服务器的定时开机与关机任务">
      <template #actions>
        <Button variant="primary" @click="openCreate">新建任务</Button>
      </template>
    </PageHeader>

    <!-- Loading -->
    <template v-if="store.loading && store.schedules.length === 0">
      <SkeletonLoader :count="4" />
    </template>

    <!-- Error -->
    <Alert v-else-if="store.error" type="danger">
      {{ store.error }}
      <template #action>
        <Button variant="danger" size="sm" @click="store.fetchSchedules()">重试</Button>
      </template>
    </Alert>

    <!-- Empty -->
    <EmptyState
      v-else-if="store.schedules.length === 0"
      description="暂无定时任务"
      actionText="新建任务"
      @action="openCreate"
    />

    <!-- Schedule Table -->
    <div v-else class="schedule-table-wrap">
      <Table :columns="columns" :data="store.schedules">
        <template #cell-action="{ row }">
          <Badge :variant="row.action === 'start' ? 'success' : 'danger'">
            {{ row.action === 'start' ? '开机' : '关机' }}
          </Badge>
        </template>
        <template #cell-nextRunAt="{ row }">
          {{ row.nextRunAt ? dayjs(row.nextRunAt).format('YYYY-MM-DD HH:mm') : '-' }}
        </template>
        <template #cell-enabled="{ row }">
          <Switch
            :modelValue="row.enabled"
            @update:modelValue="(val: boolean) => store.toggleScheduleAction(row.id, val)"
          />
        </template>
        <template #cell-operations="{ row }">
          <div class="table-actions">
            <Button variant="ghost" size="sm" @click="openEdit(row as any)">编辑</Button>
            <Button variant="ghost" size="sm" @click="handleDelete(row as any)">删除</Button>
          </div>
        </template>
      </Table>
    </div>

    <!-- Schedule Form Dialog -->
    <ScheduleForm
      v-model="dialogVisible"
      :schedule="editingSchedule"
      :servers="servers"
      @submit="handleFormSubmit"
    />

    <!-- Delete Confirm -->
    <ConfirmDialog
      v-model:modelValue="deleteDialogVisible"
      title="删除定时任务"
      :message="`确定要删除定时任务「${deletingName}」吗？`"
      type="warning"
      confirmText="确认删除"
      @confirm="handleDeleteConfirm"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useScheduleStore, useServerStore } from '@/stores'
import { PageHeader, EmptyState, SkeletonLoader, ConfirmDialog } from '@/components/common'
import ScheduleForm from '@/components/schedule/ScheduleForm.vue'
import { Button, Table, Badge, Switch, Alert } from '@/components/ui'
import type { TableColumn } from '@/components/ui'
import dayjs from 'dayjs'
import type { Schedule, ScheduleFormData } from '@/types'

const store = useScheduleStore()
const serverStore = useServerStore()
const servers = computed(() => serverStore.servers)

const dialogVisible = ref(false)
const editingSchedule = ref<Schedule | null>(null)
const deleteDialogVisible = ref(false)
const deletingId = ref('')
const deletingName = ref('')

function cronToHuman(cron: string): string {
  const parts = cron.trim().split(/\s+/)
  if (parts.length !== 5) return cron
  const [m, h, , , dow] = parts
  const time = `${h.padStart(2, '0')}:${m.padStart(2, '0')}`
  if (dow === '1-5') return `工作日 ${time}`
  if (dow === '*') return `每天 ${time}`
  if (dow === '0,6' || dow === '6,0') return `周末 ${time}`
  const dayLabels: Record<string, string> = { '1':'一','2':'二','3':'三','4':'四','5':'五','6':'六','0':'日' }
  const days = dow.split(',').map((d: string) => dayLabels[d] || d).join('、')
  return `每周${days} ${time}`
}

const columns: TableColumn[] = [
  { key: 'name', label: '任务名称', width: '140px' },
  { key: 'serverName', label: '目标服务器', width: '140px' },
  { key: 'action', label: '动作', width: '80px' },
  { key: 'cronExpression', label: '执行时间', width: '160px', formatter: (v: string) => cronToHuman(v) },
  { key: 'nextRunAt', label: '下次执行', width: '180px' },
  { key: 'enabled', label: '状态', width: '100px' },
  { key: 'operations', label: '操作', width: '120px' },
]

function openCreate() {
  editingSchedule.value = null
  dialogVisible.value = true
}

function openEdit(schedule: Schedule) {
  editingSchedule.value = schedule
  dialogVisible.value = true
}

async function handleFormSubmit(data: ScheduleFormData) {
  try {
    if (editingSchedule.value) {
      await store.updateScheduleAction(editingSchedule.value.id, data)
    } else {
      await store.createScheduleAction(data)
    }
    dialogVisible.value = false
  } catch {
    // error handled by store
  }
}

function handleDelete(schedule: Schedule) {
  deletingId.value = schedule.id
  deletingName.value = schedule.name
  deleteDialogVisible.value = true
}

async function handleDeleteConfirm() {
  await store.deleteScheduleAction(deletingId.value)
  deleteDialogVisible.value = false
}

onMounted(() => {
  store.fetchSchedules()
  serverStore.fetchServers()
})
</script>

<style scoped lang="scss">
.schedule-table-wrap {
  margin-top: 0;
}

.schedule-table-wrap :deep(.table-wrap) {
  background: var(--color-bg-card);
}

.table-actions {
  display: flex;
  gap: 4px;
}
</style>
