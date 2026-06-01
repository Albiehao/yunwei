<template>
  <el-card class="service-card" shadow="hover">
    <div class="service-card-header">
      <div class="service-info">
        <el-icon :size="24" :color="categoryColor"><component :is="categoryIcon" /></el-icon>
        <div>
          <h4 class="service-name">{{ service.name }}</h4>
          <p class="service-desc">{{ service.description }}</p>
        </div>
      </div>
      <div class="service-status-area">
        <StatusBadge :status="service.enabled ? 'enabled' : 'disabled'" />
        <el-switch
          :model-value="service.enabled"
          :loading="toggling"
          @change="handleToggle"
          :disabled="toggling"
        />
      </div>
    </div>
    <div class="service-card-footer">
      <span class="service-cost">
        预估月费：<strong>¥{{ service.monthlyCost.toFixed(2) }}</strong>
      </span>
      <span class="service-category-tag">
        <el-tag :type="categoryTagType" size="small">{{ categoryLabel }}</el-tag>
      </span>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { PayAsYouGoService, ServiceCategory } from '@/types'
import { ServiceCategory as SC } from '@/types'
import { StatusBadge } from '@/components/common'
import { FolderOpened, Connection, Coin, WarningFilled, Monitor } from '@element-plus/icons-vue'

const props = defineProps<{
  service: PayAsYouGoService
}>()

const emit = defineEmits<{
  toggle: [id: string, enabled: boolean]
}>()

const toggling = ref(false)

const categoryMap: Record<ServiceCategory, { icon: any; label: string; color: string; tagType: string }> = {
  [SC.Storage]:  { icon: FolderOpened, label: '存储', color: '#409eff', tagType: 'primary' },
  [SC.Network]:  { icon: Connection, label: '网络', color: '#67c23a', tagType: 'success' },
  [SC.Database]: { icon: Coin, label: '数据库', color: '#e6a23c', tagType: 'warning' },
  [SC.Security]: { icon: WarningFilled, label: '安全', color: '#f56c6c', tagType: 'danger' },
  [SC.Compute]:  { icon: Monitor, label: '计算', color: '#909399', tagType: 'info' },
}

const categoryInfo = computed(() => categoryMap[props.service.category] || categoryMap[SC.Compute])
const categoryIcon = computed(() => categoryInfo.value.icon)
const categoryColor = computed(() => categoryInfo.value.color)
const categoryLabel = computed(() => categoryInfo.value.label)
const categoryTagType = computed(() => categoryInfo.value.tagType)

async function handleToggle(val: boolean) {
  toggling.value = true
  emit('toggle', props.service.id, val)
  toggling.value = false
}
</script>

<style scoped lang="scss">
.service-card {
  margin-bottom: 12px;
}
.service-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}
.service-info {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  flex: 1;
}
.service-name {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
}
.service-desc {
  margin: 2px 0 0;
  font-size: 13px;
  color: var(--el-text-color-secondary);
}
.service-status-area {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}
.service-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-light);
}
.service-cost {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  strong {
    color: var(--el-color-primary);
    font-size: 15px;
  }
}
</style>
