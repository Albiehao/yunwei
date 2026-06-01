<template>
  <div class="server-list-page">
    <PageHeader title="我的服务器" />

    <!-- Summary bar -->
    <div v-if="!store.loading && store.servers.length > 0" class="summary-bar">
      <div class="summary-item"><span class="sum-num">{{ store.servers.length }}</span> 总计</div>
      <div class="summary-item"><span class="sum-num sum-running">{{ store.runningServers.length }}</span> 运行中</div>
      <div class="summary-item"><span class="sum-num sum-stopped">{{ store.stoppedServers.length }}</span> 已停止</div>
    </div>

    <!-- Loading -->
    <template v-if="store.loading && store.servers.length === 0">
      <div v-for="i in 3" :key="i" class="card-loading">
        <SkeletonLoader :count="2" />
      </div>
    </template>

    <!-- Error -->
    <Alert v-else-if="store.error" type="danger" style="margin-bottom:12px">
      {{ store.error }}
      <template #action>
        <Button variant="danger" size="sm" @click="handleRefresh">重试</Button>
      </template>
    </Alert>

    <!-- Search + Region -->
    <div v-if="store.servers.length > 0" class="search-bar">
      <Input v-model="searchQuery" placeholder="搜索服务器..." prefix-icon="search" />
      <Select v-model="selectedRegion" :options="regionOptions" placeholder="地域" />
      <Button variant="ghost" @click="handleRefresh">刷新</Button>
    </div>

    <!-- Empty -->
    <EmptyState v-if="store.servers.length === 0 && !store.loading" description="暂无服务器" />

    <!-- Server List -->
    <div v-if="filteredServers.length > 0" class="server-list">
      <ServerCard v-for="(s, idx) in filteredServers" :key="s.id" :server="s" :style="{ '--i': idx }" @start="handleStart" @stop="handleStop" @release="handleRelease" @namechange="handleNameChange" />
    </div>
    <div v-else-if="store.servers.length > 0 && !store.loading" style="text-align:center;padding:32px;color:var(--color-text-muted)">没有匹配的服务器</div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue'
import { useServerStore } from '@/stores'
import { PageHeader, EmptyState, SkeletonLoader } from '@/components/common'
import { ServerCard } from '@/components/server'
import { Button, Input, Select, Alert } from '@/components/ui'

const store = useServerStore()
const searchQuery = ref('')
const selectedRegion = ref('')

const regionOptions = [
  { label: '华东1 (杭州)', value: 'cn-hangzhou' },
  { label: '华东2 (上海)', value: 'cn-shanghai' },
  { label: '华北1 (青岛)', value: 'cn-qingdao' },
  { label: '华北2 (北京)', value: 'cn-beijing' },
  { label: '华北3 (张家口)', value: 'cn-zhangjiakou' },
  { label: '华南1 (深圳)', value: 'cn-shenzhen' },
  { label: '香港', value: 'cn-hongkong' },
  { label: '新加坡', value: 'ap-southeast-1' },
  { label: '日本 (东京)', value: 'ap-northeast-1' },
  { label: '美国 (硅谷)', value: 'us-west-1' },
]

const filteredServers = computed(() => {
  if (!searchQuery.value) return store.servers
  return store.servers.filter(s =>
    s.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

watch(selectedRegion, (region) => {
  store.fetchServers(region)
})

function handleRefresh() {
  store.fetchServers(selectedRegion.value)
}

async function handleStart(id: string) {
  await store.startServerAction(id)
}

async function handleStop(id: string, mode: string) {
  await store.stopServerAction(id, mode)
}

async function handleRelease(id: string) {
  await store.releaseServerAction(id)
}

function handleNameChange(id: string, remark: string) {
  const s = store.servers.find(x => x.id === id)
  if (s) s.remark = remark
}

onMounted(() => {
  store.fetchServers()
})
</script>

<style scoped lang="scss">
.search-bar {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 14px 18px;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: var(--shadow-glass);
}

.search-bar :deep(.input-wrap) { flex: 1; min-width: 200px; }
.search-bar :deep(.select-wrap) { width: auto; min-width: 100px; max-width: 160px; }
.search-bar :deep(.select-wrap) { min-width: 160px; }

.card-loading {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 16px;
}

.server-list {
  margin-top: 12px;
}

.summary-bar {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  padding: 16px 20px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
}
.summary-item {
  font-size: 13px;
  color: var(--color-text-secondary);
}
.sum-num {
  font-size: 22px;
  font-weight: 700;
  color: var(--color-text);
  margin-right: 4px;
}
.sum-running { color: var(--color-success); }
.sum-stopped { color: var(--color-text-muted); }
</style>
