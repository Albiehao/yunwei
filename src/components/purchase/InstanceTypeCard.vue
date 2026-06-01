<template>
  <el-card
    class="instance-card"
    :class="{ 'is-selected': selected }"
    shadow="hover"
    @click="$emit('select')"
  >
    <div class="instance-card-header">
      <h4 class="instance-name">{{ instance.name }}</h4>
      <el-tag size="small" v-if="instance.family === '通用型'">推荐</el-tag>
    </div>
    <p class="instance-desc">{{ instance.description }}</p>
    <div class="instance-specs">
      <div class="spec"><el-icon><Cpu /></el-icon> {{ instance.cpu }} vCPU</div>
      <div class="spec"><el-icon><Monitor /></el-icon> {{ instance.memory }} GB</div>
      <div class="spec"><el-icon><DataBoard /></el-icon> {{ instance.disk }} GB</div>
      <div class="spec"><el-icon><Connection /></el-icon> {{ instance.bandwidth }} Mbps</div>
    </div>
    <div class="instance-price">
      <span class="price-amount">¥{{ instance.hourlyPrice }}/时</span>
      <span class="price-monthly">约 ¥{{ (instance.hourlyPrice * 24 * 30).toFixed(0) }}/月</span>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import type { InstanceType } from '@/types'
import { Cpu, Monitor, DataBoard, Connection } from '@element-plus/icons-vue'

defineProps<{
  instance: InstanceType
  selected?: boolean
}>()

defineEmits<{
  select: []
}>()
</script>

<style scoped lang="scss">
.instance-card {
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;

  &:hover {
    border-color: var(--el-color-primary-light-5);
  }

  &.is-selected {
    border-color: var(--el-color-primary);
    background-color: var(--el-color-primary-light-9);
  }
}
.instance-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.instance-name {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}
.instance-desc {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  margin: 4px 0 12px;
}
.instance-specs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 12px;
}
.spec {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--el-text-color-regular);
}
.instance-price {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-light);
}
.price-amount {
  font-size: 20px;
  font-weight: 700;
  color: var(--el-color-primary);
}
.price-monthly {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}
</style>
