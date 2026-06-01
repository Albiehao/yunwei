<template>
  <div class="skeleton-loader" :style="{ width, height }">
    <div class="skeleton-item" :style="{ height: itemHeight }"></div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  width?: string
  height?: string
  itemHeight?: string
  count?: number
}>(), {
  width: '100%',
  height: '20px',
  itemHeight: '20px',
  count: 3
})
</script>

<style scoped lang="scss">
.skeleton-loader {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.skeleton-item {
  background: linear-gradient(90deg,
    var(--el-skeleton-color) 25%,
    var(--el-skeleton-to-color) 37%,
    var(--el-skeleton-color) 63%
  );
  background-size: 400% 100%;
  animation: skeleton-loading 1.4s ease infinite;
  border-radius: 4px;
  width: 100%;
}
@keyframes skeleton-loading {
  0% { background-position: 100% 50%; }
  100% { background-position: 0 50%; }
}
</style>
