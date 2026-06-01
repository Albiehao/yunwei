<template>
  <div class="server-controls">
    <el-button
      v-if="status === ServerStatus.Stopped || status === ServerStatus.Error"
      type="success"
      size="small"
      :loading="status === ServerStatus.Starting"
      :icon="VideoPlay"
      @click="$emit('start')"
      :disabled="status === ServerStatus.Starting"
    >
      启动
    </el-button>
    <el-button
      v-if="status === ServerStatus.Running"
      type="danger"
      size="small"
      :loading="status === ServerStatus.Stopping"
      :icon="VideoPause"
      @click="$emit('stop')"
      :disabled="status === ServerStatus.Stopping"
    >
      停止
    </el-button>
    <el-tag
      v-if="status === ServerStatus.Starting"
      type="warning"
      size="small"
      effect="plain"
    >
      启动中...
    </el-tag>
    <el-tag
      v-if="status === ServerStatus.Stopping"
      type="warning"
      size="small"
      effect="plain"
    >
      停止中...
    </el-tag>
  </div>
</template>

<script setup lang="ts">
import { ServerStatus } from '@/types'
import { VideoPlay, VideoPause } from '@element-plus/icons-vue'

defineProps<{
  status: ServerStatus
}>()

defineEmits<{
  start: []
  stop: []
}>()
</script>

<style scoped lang="scss">
.server-controls {
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>
