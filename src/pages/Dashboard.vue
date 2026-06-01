<template>
  <div class="dashboard">
    <PageHeader title="控制台" description="云服务运维概览" />

    <!-- Loading -->
    <template v-if="loading">
      <el-row :gutter="16">
        <el-col :span="6" v-for="i in 4" :key="i">
          <el-card><SkeletonLoader :count="2" /></el-card>
        </el-col>
      </el-row>
    </template>

    <!-- Summary Cards -->
    <el-row :gutter="16" class="summary-row">
      <el-col :span="6">
        <el-card class="summary-card" shadow="hover">
          <div class="card-content">
            <div class="card-icon server-icon">
              <el-icon :size="24"><Monitor /></el-icon>
            </div>
            <div class="card-info">
              <p class="card-value">{{ serverStore.serverCount }}</p>
              <p class="card-label">总服务器</p>
            </div>
          </div>
          <div class="card-footer">
            <span class="running-count">{{ serverStore.runningServers.length }} 台运行中</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="summary-card" shadow="hover">
          <div class="card-content">
            <div class="card-icon service-icon">
              <el-icon :size="24"><Coin /></el-icon>
            </div>
            <div class="card-info">
              <p class="card-value">{{ serviceStore.activeServices.length }}</p>
              <p class="card-label">启用服务</p>
            </div>
          </div>
          <div class="card-footer">
            <span class="cost-text">¥{{ serviceStore.totalMonthlyCost.toFixed(2) }}/月</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="summary-card" shadow="hover">
          <div class="card-content">
            <div class="card-icon schedule-icon">
              <el-icon :size="24"><Clock /></el-icon>
            </div>
            <div class="card-info">
              <p class="card-value">{{ scheduleStore.enabledSchedules.length }}</p>
              <p class="card-label">定时任务</p>
            </div>
          </div>
          <div class="card-footer">
            <span>{{ scheduleStore.schedules.length }} 个总任务</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="summary-card" shadow="hover">
          <div class="card-content">
            <div class="card-icon running-icon">
              <el-icon :size="24"><VideoPlay /></el-icon>
            </div>
            <div class="card-info">
              <p class="card-value">{{ serverStore.runningServers.length }}</p>
              <p class="card-label">运行中</p>
            </div>
          </div>
          <div class="card-footer">
            <span>{{ ((serverStore.runningServers.length / Math.max(serverStore.serverCount, 1)) * 100).toFixed(0) }}% 在线率</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Server List -->
    <el-card class="section-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>服务器列表</span>
          <el-button text type="primary" @click="$router.push('/servers')">查看全部</el-button>
        </div>
      </template>
      <el-table :data="serverStore.servers.slice(0, 5)" stripe v-if="serverStore.servers.length > 0">
        <el-table-column prop="name" label="名称" min-width="140" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <StatusBadge :status="row.status" />
          </template>
        </el-table-column>
        <el-table-column prop="instanceType" label="规格" width="120" />
        <el-table-column prop="ipAddress" label="IP 地址" width="140" />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <ServerControls
              :status="row.status"
              @start="serverStore.startServerAction(row.id)"
              @stop="serverStore.stopServerAction(row.id)"
            />
          </template>
        </el-table-column>
      </el-table>
      <EmptyState v-else description="暂无服务器" actionText="购买服务器" @action="$router.push('/purchase')" />
    </el-card>

    <!-- Schedule List -->
    <el-card class="section-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>近期定时任务</span>
          <el-button text type="primary" @click="$router.push('/schedules')">查看全部</el-button>
        </div>
      </template>
      <el-table :data="scheduleStore.enabledSchedules.slice(0, 4)" stripe v-if="scheduleStore.enabledSchedules.length > 0">
        <el-table-column prop="name" label="任务名称" min-width="140" />
        <el-table-column prop="serverName" label="目标服务器" width="140" />
        <el-table-column label="动作" width="80">
          <template #default="{ row }">
            <el-tag :type="row.action === 'start' ? 'success' : 'danger'" size="small">
              {{ row.action === 'start' ? '开机' : '关机' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="下次执行" width="180">
          <template #default="{ row }">
            {{ row.nextRunAt ? dayjs(row.nextRunAt).format('MM-DD HH:mm') : '-' }}
          </template>
        </el-table-column>
      </el-table>
      <EmptyState v-else description="暂无定时任务" actionText="新建任务" @action="$router.push('/schedules')" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useServerStore, useServiceStore, useScheduleStore } from '@/stores'
import { PageHeader, EmptyState, SkeletonLoader, StatusBadge } from '@/components/common'
import { ServerControls } from '@/components/server'
import { Monitor, Coin, Clock, VideoPlay } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const serverStore = useServerStore()
const serviceStore = useServiceStore()
const scheduleStore = useScheduleStore()

const loading = computed(() =>
  serverStore.loading || serviceStore.loading || scheduleStore.loading
)

onMounted(() => {
  serverStore.fetchServers()
  serviceStore.fetchServices()
  scheduleStore.fetchSchedules()
})
</script>

<style scoped lang="scss">
.summary-row {
  margin-bottom: 24px;
}
.summary-card {
  .card-content {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .card-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .server-icon { background: rgba(64,158,255,0.1); color: #409eff; }
  .service-icon { background: rgba(103,194,58,0.1); color: #67c23a; }
  .schedule-icon { background: rgba(230,162,60,0.1); color: #e6a23c; }
  .running-icon { background: rgba(96,98,102,0.1); color: #606266; }
  .card-value {
    font-size: 28px;
    font-weight: 700;
    margin: 0;
    line-height: 1.2;
  }
  .card-label {
    font-size: 13px;
    color: var(--el-text-color-secondary);
    margin: 4px 0 0;
  }
  .card-footer {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--el-border-color-light);
    font-size: 12px;
    color: var(--el-text-color-secondary);
  }
}
.section-card {
  margin-bottom: 16px;
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
  }
}
</style>
