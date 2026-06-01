<template>
  <div class="service-batch-controls">
    <el-button
      :type="allEnabled ? 'danger' : 'success'"
      :icon="allEnabled ? 'VideoPause' : 'VideoPlay'"
      :loading="loading"
      @click="handleBatchToggle"
    >
      {{ allEnabled ? '全部停用' : '全部启用' }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  allEnabled: boolean
  loading: boolean
}>()

const emit = defineEmits<{
  batchToggle: [enabled: boolean]
}>()

function handleBatchToggle() {
  // pass
}
</script>
