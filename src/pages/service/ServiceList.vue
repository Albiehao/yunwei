<template>
  <div class="service-list-page">
    <PageHeader title="按量服务" description="管理按量付费云服务，按实际使用量计费">
      <template #actions>
        <el-tag type="info" effect="plain" size="large">
          预估月费：<strong>¥{{ store.totalMonthlyCost.toFixed(2) }}</strong>
        </el-tag>
      </template>
    </PageHeader>

    <!-- Loading -->
    <template v-if="store.loading && store.services.length === 0">
      <el-card v-for="i in 3" :key="i" style="margin-bottom:12px">
        <SkeletonLoader :count="2" />
      </el-card>
    </template>

    <!-- Error -->
    <el-alert
      v-else-if="store.error"
      :title="store.error"
      type="error" show-icon
      :closable="false"
    >
      <template #action>
        <el-button size="small" type="danger" @click="store.fetchServices()">重试</el-button>
      </template>
    </el-alert>

    <!-- Empty -->
    <EmptyState
      v-else-if="store.services.length === 0"
      description="暂无按量服务"
    />

    <!-- Service List -->
    <div v-else class="service-summary">
      <el-row :gutter="12" class="summary-cards">
        <el-col :span="6" v-for="cat in categoryStats" :key="cat.label">
          <el-card shadow="never" class="summary-card">
            <div class="summary-card-inner">
              <el-icon :size="20" :color="cat.color"><component :is="cat.icon" /></el-icon>
              <div>
                <p class="summary-num">{{ cat.count }}</p>
                <p class="summary-label">{{ cat.label }}</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div v-if="store.services.length > 0" class="service-list">
      <ServiceCard
        v-for="service in store.services"
        :key="service.id"
        :service="service"
        @toggle="handleToggle"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useServiceStore } from '@/stores'
import { ServiceCategory as SC } from '@/types'
import { PageHeader, EmptyState, SkeletonLoader } from '@/components/common'
import { ServiceCard } from '@/components/service'
import { FolderOpened, Connection, Coin, WarningFilled, Monitor } from '@element-plus/icons-vue'

const store = useServiceStore()

const categoryStats = computed(() => {
  const cats = [
    { label: '存储服务', key: SC.Storage, icon: FolderOpened, color: '#409eff' },
    { label: '网络服务', key: SC.Network, icon: Connection, color: '#67c23a' },
    { label: '数据库/中间件', key: SC.Database, icon: Coin, color: '#e6a23c' },
    { label: '安全服务', key: SC.Security, icon: WarningFilled, color: '#f56c6c' },
  ]
  return cats.map(c => ({
    ...c,
    count: store.services.filter(s => s.category === c.key).length
  }))
})

async function handleToggle(id: string, enabled: boolean) {
  await store.toggleService(id, enabled)
}

onMounted(() => {
  store.fetchServices()
})
</script>

<style scoped lang="scss">
.service-summary {
  margin-bottom: 16px;
}
.summary-card-inner {
  display: flex;
  align-items: center;
  gap: 12px;
}
.summary-num {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}
.summary-label {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  margin: 0;
}
</style>
