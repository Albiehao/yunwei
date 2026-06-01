<template>
  <div class="release-page">
    <PageHeader title="释放实例" description="管理按量付费实例，释放后数据永久删除" />

    <template v-if="loading">
      <div v-for="i in 2" :key="i" class="card-loading">
        <SkeletonLoader :count="2" />
      </div>
    </template>

    <Alert v-else-if="error" type="danger" style="margin-bottom:12px">
      {{ error }}
      <template #action>
        <Button variant="danger" size="sm" @click="loadData">重试</Button>
      </template>
    </Alert>

    <template v-else-if="candidates.length === 0">
      <EmptyState description="没有可释放的按量实例" />
    </template>

    <div v-else class="release-list">
      <div v-for="s in candidates" :key="s.id" class="release-card">
        <div class="release-info">
          <h3 class="release-name">{{ s.name }}</h3>
          <div class="release-meta">
            <span>{{ s.instanceType }}</span>
            <span>{{ s.region }}</span>
            <span>{{ s.ipAddress || '无IP' }}</span>
            <Badge :variant="s.status === 'running' ? 'success' : 'default'">
              {{ s.status === 'running' ? '运行中' : '已停止' }}
            </Badge>
          </div>
        </div>
        <Button variant="danger" size="sm" :loading="targetId === s.id" @click="handleRelease(s)">
          释放
        </Button>
      </div>
    </div>

    <ConfirmDialog
      v-model:modelValue="dialogVisible"
      title="释放实例"
      :message="`确定要释放「${targetName}」吗？释放后所有数据永久删除，不可恢复！`"
      type="danger"
      confirmText="确认释放"
      @confirm="confirmRelease"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useServerStore, useTaskStore } from '@/stores'
import { PageHeader, EmptyState, SkeletonLoader, ConfirmDialog } from '@/components/common'
import { Button, Alert, Badge } from '@/components/ui'

const router = useRouter()
const store = useServerStore()
const taskStore = useTaskStore()
const loading = ref(false)
const error = ref('')
const dialogVisible = ref(false)
const targetId = ref('')
const targetName = ref('')

const candidates = computed(() =>
  store.servers.filter(s => s.chargeType === 'PostPaid')
)

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    await store.fetchServers()
  } catch {
    error.value = '加载失败'
  } finally {
    loading.value = false
  }
}

function handleRelease(s: any) {
  targetId.value = s.id
  targetName.value = s.name
  dialogVisible.value = true
}

async function confirmRelease() {
  dialogVisible.value = false
  try {
    await taskStore.createRelease(targetId.value, targetName.value)
    router.push('/tasks')
  } catch {
    error.value = '创建任务失败'
  }
}

onMounted(loadData)
</script>

<style scoped lang="scss">
.release-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 16px 20px;
  margin-bottom: 12px;
  gap: 16px;
}

.release-name {
  font-size: 15px;
  font-weight: 600;
  margin: 0 0 6px;
}

.release-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.card-loading {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 16px;
}
</style>
