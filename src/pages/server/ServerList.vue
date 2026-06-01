<template>
  <div class="server-list-page">
    <PageHeader title="服务器管理" description="管理与监控所有云服务器实例">
      <template #actions>
        <el-button type="primary" :icon="Plus" @click="handleCreate">
          创建实例
        </el-button>
      </template>
    </PageHeader>

    <!-- Loading State -->
    <template v-if="store.loading && store.servers.length === 0">
      <el-card v-for="i in 3" :key="i" style="margin-bottom: 16px;">
        <SkeletonLoader :count="2" />
      </el-card>
    </template>

    <!-- Error State -->
    <el-alert
      v-else-if="store.error"
      :title="store.error"
      type="error"
      show-icon
      :closable="false"
    >
      <template #action>
        <el-button size="small" type="danger" @click="store.fetchServers()">重试</el-button>
      </template>
    </el-alert>

    <!-- Search Bar -->
    <template v-else-if="store.servers.length > 0">
      <el-card class="search-bar" shadow="never">
        <el-row :gutter="16">
          <el-col :span="6">
            <el-input v-model="searchQuery" placeholder="搜索服务器名称" clearable :prefix-icon="Search" />
          </el-col>
          <el-col :span="4">
            <el-select v-model="statusFilter" placeholder="状态筛选" clearable style="width:100%">
              <el-option label="运行中" value="running" />
              <el-option label="已停止" value="stopped" />
              <el-option label="异常" value="error" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-select v-model="chargeFilter" placeholder="付费类型" clearable style="width:100%">
              <el-option label="按量付费" value="PostPaid" />
              <el-option label="包年包月" value="PrePaid" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-button :icon="Refresh" @click="store.fetchServers()">刷新</el-button>
          </el-col>
        </el-row>
      </el-card>
    </template>

    <!-- Empty State -->
    <EmptyState
      v-else
      description="暂无服务器实例"
      actionText="立即创建"
      @action="handleCreate"
    />

    <!-- Server List -->
    <div v-if="filteredServers.length > 0" class="server-list">
      <ServerCard
        v-for="server in filteredServers"
        :key="server.id"
        :server="server"
        @start="handleStart"
        @stop="handleStop"
      />
    </div>
    <EmptyState
      v-else-if="store.servers.length > 0 && !store.loading"
      type="search"
      description="没有匹配的服务器"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useServerStore } from '@/stores'
import { PageHeader, EmptyState, SkeletonLoader } from '@/components/common'
import { ServerCard } from '@/components/server'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'

const router = useRouter()
const store = useServerStore()
const searchQuery = ref('')
const statusFilter = ref('')
const chargeFilter = ref('')

const filteredServers = computed(() => {
  return store.servers.filter(s => {
    if (searchQuery.value && !s.name.toLowerCase().includes(searchQuery.value.toLowerCase())) return false
    if (statusFilter.value && s.status !== statusFilter.value) return false
    if (chargeFilter.value && s.chargeType !== chargeFilter.value) return false
    return true
  })
})

function handleCreate() {
  router.push('/purchase')
}

async function handleStart(id: string) {
  await store.startServerAction(id)
}

async function handleStop(id: string) {
  await store.stopServerAction(id)
}

onMounted(() => {
  store.fetchServers()
})
</script>

<style scoped lang="scss">
.search-bar {
  margin-bottom: 16px;
}
.server-list {
  margin-top: 16px;
}
</style>
