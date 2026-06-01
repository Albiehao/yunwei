<template>
  <div class="empty-state">
    <el-icon :size="64" color="var(--el-text-color-placeholder)">
      <Icon :is="iconComponent" />
    </el-icon>
    <p class="empty-text">{{ description }}</p>
    <el-button v-if="actionText" type="primary" @click="$emit('action')">
      {{ actionText }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { FolderDelete, Search, Files, FolderOpened } from '@element-plus/icons-vue'

const props = withDefaults(defineProps<{
  type?: 'empty' | 'search' | 'file'
  description?: string
  actionText?: string
}>(), {
  type: 'empty',
  description: '暂无数据'
})

defineEmits<{
  action: []
}>()

const iconComponent = computed(() => {
  const icons = { empty: FolderDelete, search: Search, file: Files }
  return icons[props.type] || FolderOpened
})
</script>

<style scoped lang="scss">
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 16px;
}
.empty-text {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}
</style>
