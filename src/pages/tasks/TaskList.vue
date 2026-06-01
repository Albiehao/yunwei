<template>
  <div class="page">
    <PageHeader title="任务列表" description="待执行的释放任务" />

    <template v-if="store.loading">
      <div v-for="i in 2" :key="i" class="card-loading"><SkeletonLoader :count="2" /></div>
    </template>

    <template v-else-if="store.tasks.length === 0">
      <EmptyState description="暂无任务" />
    </template>

    <div v-else class="task-list">
      <div v-for="t in store.tasks" :key="t.id" class="task-card" :class="`task-${t.status}`">
        <div class="task-left">
          <div class="task-top">
            <Badge :variant="statusBadge(t.status)">{{ statusLabel(t.status) }}</Badge>
            <span class="task-action">{{ actionLabel(t.action) }}</span>
          </div>
          <div class="task-server">{{ t.serverName || t.serverId || (t.params?.name || '') }}</div>
          <div class="task-time" v-if="t.params?.instanceType">{{ t.params.instanceType }} x{{ t.params.quantity || 1 }} | {{ formatTime(t.createdAt) }}</div>
          <div class="task-time" v-else>{{ formatTime(t.createdAt) }}</div>
        </div>
        <div class="task-right">
          <template v-if="t.status === 'pending'">
            <Button variant="danger" size="sm" @click="confirmExecute(t)">执行</Button>
            <Button variant="ghost" size="sm" @click="handleDelete(t)">删除</Button>
          </template>
          <template v-else>
            <span class="task-msg">{{ t.message }}</span>
            <Button variant="ghost" size="sm" @click="handleDelete(t)">删除</Button>
          </template>
        </div>
      </div>
    </div>

    <ConfirmDialog
      v-if="execTarget"
      :model-value="true"
      title="确认执行"
      :message="execTarget.action === 'release' ? `释放后数据将永久删除！确定释放「${execTarget.serverName}」？` : execTarget.action === 'purchase' ? `管理员确认购买 ${execTarget.params?.instanceType || ''} x${execTarget.params?.quantity || 1} ？` : `确定执行？`"
      type="danger"
      confirmText="确认执行"
      @confirm="doExecute"
      @cancel="execTarget = null"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTaskStore } from '@/stores'
import type { TaskItem } from '@/stores/task'
import { PageHeader, EmptyState, SkeletonLoader, ConfirmDialog } from '@/components/common'
import { Button, Badge } from '@/components/ui'

const store = useTaskStore()
const execTarget = ref<TaskItem | null>(null)

function statusLabel(s: string) {
  return { pending: '待执行', done: '已完成', failed: '失败' }[s] || s
}
function statusBadge(s: string): "success" | "danger" | "warning" | "default" | "primary" | "info" {
  return { pending: 'warning', done: 'success', failed: 'danger' }[s] || 'default'
}
function actionLabel(a: string) {
  return { release: '释放实例', purchase: '购买服务器' }[a] || a
}
function formatTime(iso: string) {
  if (!iso) return '-'
  return iso.slice(0, 19).replace('T', ' ')
}

function confirmExecute(t: TaskItem) {
  execTarget.value = t
}

async function doExecute() {
  if (!execTarget.value) return
  await store.executeTask(execTarget.value.id)
  execTarget.value = null
}

function handleDelete(t: TaskItem) {
  store.deleteTask(t.id)
}

onMounted(() => store.fetchTasks())
</script>

<style scoped lang="scss">
.task-card {
  display: flex; justify-content: space-between; align-items: center;
  background: var(--color-bg-card); border: 1px solid var(--color-border);
  border-radius: var(--radius-lg); padding: 16px 20px; margin-bottom: 10px; gap: 16px;
}
.task-left { flex: 1; }
.task-top { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.task-action { font-size: 14px; font-weight: 600; }
.task-server { font-size: 13px; color: var(--color-text-secondary); margin-bottom: 2px; }
.task-time { font-size: 12px; color: var(--color-text-muted); }
.task-right { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.task-msg { font-size: 13px; color: var(--color-text-secondary); }

.card-loading {
  background: var(--color-bg-card); border: 1px solid var(--color-border);
  border-radius: var(--radius-lg); padding: 20px; margin-bottom: 16px;
}
</style>
