<template>
  <el-container class="layout-container">
    <AppSidebar />
    <el-container class="main-container">
      <AppHeader />
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'
</script>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
}
.main-container {
  display: flex;
  flex-direction: column;
}
.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
