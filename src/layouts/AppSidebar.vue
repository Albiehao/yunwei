<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': appStore.sidebarCollapsed }">
    <div class="sidebar-brand">
      <div class="brand-icon">
        <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
          <rect width="32" height="32" rx="8" fill="var(--color-primary)"/>
          <path d="M16 8l8 4.5v7L16 24l-8-4.5v-7L16 8z" stroke="white" stroke-width="1.5" fill="none"/>
          <path d="M16 13l3 2v3l-3 2-3-2v-3l3-2z" stroke="white" stroke-width="1.5" fill="none"/>
        </svg>
      </div>
      <span v-show="!appStore.sidebarCollapsed" class="brand-text">寻天运维</span>
    </div>
    <nav class="sidebar-nav">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        :class="{ 'nav-item--active': route.path.startsWith(item.path) }"
      >
        <Icon :name="item.icon" :size="20" class="nav-icon" />
        <span v-show="!appStore.sidebarCollapsed" class="nav-label">{{ item.label }}</span>
      </router-link>
    </nav>
    <div class="sidebar-footer">
      <button class="collapse-btn" @click="appStore.toggleSidebar()">
        <Icon :name="appStore.sidebarCollapsed ? 'chevron-right' : 'chevron-left'" :size="16" />
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores'
import Icon from '@/components/ui/Icon.vue'

const route = useRoute()
const appStore = useAppStore()
const menuItems = [
  { path: '/servers', icon: 'server', label: '我的服务器' },
  { path: '/schedules', icon: 'schedule', label: '定时开关' },
  { path: '/release', icon: 'trash', label: '释放实例' },
  { path: '/tasks', icon: 'schedule', label: '任务列表' },
  { path: '/logs', icon: 'schedule', label: '操作日志' },
  { path: '/users', icon: 'user', label: '用户管理' },
]
</script>

<style scoped lang="scss">
.sidebar {
  width: var(--sidebar-width);
  background: var(--glass-sidebar);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border-right: 1px solid var(--glass-sidebar-border);
  display: flex;
  flex-direction: column;
  transition: width var(--transition-smooth);
  overflow: hidden;
  flex-shrink: 0;

  &--collapsed { width: var(--sidebar-collapsed-width); }
}

.sidebar-brand {
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 10px;
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.brand-icon { flex-shrink: 0; display: flex; }

.brand-text {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text);
  white-space: nowrap;
  letter-spacing: -0.3px;
}

.sidebar-nav {
  flex: 1;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: var(--radius-lg);
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all var(--transition);
  white-space: nowrap;

  &:hover {
    color: var(--color-text);
    background: var(--color-bg-hover);
  }

  &--active {
    color: var(--color-primary);
    background: var(--color-primary-bg);
    font-weight: 600;
  }
}

.nav-icon { flex-shrink: 0; }
.nav-label { font-size: 14px; }

.sidebar-footer {
  padding: 8px;
  border-top: 1px solid var(--color-border);
}

.collapse-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition);
  &:hover { background: var(--color-bg-hover); color: var(--color-text); }
}
</style>
