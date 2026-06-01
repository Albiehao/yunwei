<template>
  <el-menu
    :default-active="route.path"
    :collapse="appStore.sidebarCollapsed"
    :router="true"
    class="sidebar-menu"
    background-color="var(--el-menu-bg-color)"
    text-color="var(--el-menu-text-color)"
    active-text-color="var(--el-color-primary)"
  >
    <div class="sidebar-logo">
      <el-icon :size="28"><Monitor /></el-icon>
      <span v-show="!appStore.sidebarCollapsed" class="logo-text">云服务运维</span>
    </div>

    <el-menu-item
      v-for="item in menuItems"
      :key="item.path"
      :index="item.path"
    >
      <el-icon><component :is="item.icon" /></el-icon>
      <template #title>
        <span>{{ item.title }}</span>
      </template>
    </el-menu-item>

    <div class="sidebar-collapse-btn" @click="appStore.toggleSidebar()">
      <el-icon>
        <Fold v-if="!appStore.sidebarCollapsed" />
        <Expand v-else />
      </el-icon>
    </div>
  </el-menu>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores'
import { Monitor, Platform, Coin, Clock, ShoppingCart, Fold, Expand } from '@element-plus/icons-vue'

const route = useRoute()
const appStore = useAppStore()

const menuItems = [
  { path: '/dashboard', title: '控制台', icon: 'Monitor' },
  { path: '/servers', title: '服务器管理', icon: 'Platform' },
  { path: '/services', title: '按量服务', icon: 'Coin' },
  { path: '/schedules', title: '定时任务', icon: 'Clock' },
  { path: '/purchase', title: '购买服务器', icon: 'ShoppingCart' },
]
</script>

<style scoped lang="scss">
.sidebar-menu {
  height: 100vh;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--el-border-color-light);
  overflow: hidden;

  &:not(.el-menu--collapse) {
    width: 220px;
  }
}

.sidebar-logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border-bottom: 1px solid var(--el-border-color-light);

  .logo-text {
    font-size: 18px;
    font-weight: bold;
    white-space: nowrap;
  }
}

.sidebar-collapse-btn {
  margin-top: auto;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  border-top: 1px solid var(--el-border-color-light);

  &:hover {
    color: var(--el-color-primary);
  }
}
</style>
