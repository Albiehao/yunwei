<template>
  <div class="schedule-list-page">
    <PageHeader title="定时任务" description="设置服务器的定时开机与关机任务">
      <template #actions>
        <el-button type="primary" :icon="Plus" @click="openCreate">
          新建任务
        </el-button>
      </template>
    </PageHeader>

    <!-- Loading -->
    <template v-if="store.loading && store.schedules.length === 0">
      <SkeletonLoader :count="4" />
    </template>

    <!-- Error -->
    <el-alert
      v-else-if="store.error"
      :title="store.error"
      type="error" show-icon :closable="false"
    >
      <template #action>
        <el-button size="small" type="danger" @click="store.fetchSchedules()">重试</el-button>
      </template>
    </el-alert>

    <!-- Empty -->
    <EmptyState
      v-else-if="store.schedules.length === 0"
      description="暂无定时任务"
      actionText="新建任务"
      @action="openCreate"
    />

    <!-- Schedule Table -->
    <el-card v-else shadow="never">
      <el-table :data="store.schedules" stripe>
        <el-table-column label="任务名称" prop="name" min-width="140" />
        <el-table-column label="目标服务器" prop="serverName" min-width="140" />
        <el-table-column label="动作" width="80">
          <template #default="{ row }">
            <el-tag :type="row.action === 'start' ? 'success' : 'danger'" size="small">
              {{ row.action === 'start' ? '开机' : '关机' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Cron 表达式" prop="cronExpression" width="160" />
        <el-table-column label="下次执行" width="180">
          <template #default="{ row }">
            {{ row.nextRunAt ? dayjs(row.nextRunAt).format('YYYY-MM-DD HH:mm') : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              :model-value="row.enabled"
              size="small"
              @change="(val: boolean) => store.toggleScheduleAction(row.id, val)"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openEdit(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

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
import { Plus } from '@element-plus/icons-vue'
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

function openCreate() {
  editingSchedule.value = null
  dialogVisible.value = true
}

function openEdit(schedule: Schedule) {
  editingSchedule.value = schedule
  dialogVisible.value = true
}

async function handleFormSubmit(data: ScheduleFormData) {
  if (editingSchedule.value) {
    await store.updateScheduleAction(editingSchedule.value.id, data)
  } else {
    await store.createScheduleAction(data)
  }
  dialogVisible.value = false
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
