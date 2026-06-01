<template>
  <header class="header">
    <div class="header-left">
      <div class="breadcrumb">
        <span class="crumb crumb-current">{{ currentTitle || '寻天运维平台' }}</span>
      </div>
    </div>
    <div class="header-right">
      <button class="header-btn" @click="appStore.toggleDark()" :title="appStore.isDark ? '亮色模式' : '暗色模式'">
        <Icon :name="appStore.isDark ? 'sun' : 'moon'" :size="18" />
      </button>
      <div class="header-divider" />
      <div class="user-menu">
        <div class="user-avatar">{{ userStore.currentUser?.username?.[0]?.toUpperCase() || 'A' }}</div>
        <span class="user-name">{{ userStore.currentUser?.username || '管理员' }}</span>
      </div>
      <button class="header-btn" @click="handleLogout" title="退出登录">
        <Icon name="logout" :size="18" />
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore, useUserStore } from '@/stores'
import { Icon } from '@/components/ui'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()
const userStore = useUserStore()
const currentTitle = computed(() => route.meta?.title as string || '')

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped lang="scss">
.header {
  height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: var(--glass-header);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
  gap: 16px;
}

.header-left { flex: 1; }
.breadcrumb { display: flex; align-items: center; gap: 6px; }
.crumb { font-size: 13px; }
.crumb-current { color: var(--color-text); font-weight: 600; }

.header-right { display: flex; align-items: center; gap: 8px; }

.header-btn {
  width: 36px; height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  border-radius: var(--radius-full);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition);
  &:hover { background: var(--color-bg-hover); color: var(--color-primary); }
}

.header-divider { width: 1px; height: 20px; background: var(--color-border); }

.user-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: background var(--transition);
  &:hover { background: var(--color-bg-hover); }
}

.user-avatar {
  width: 28px; height: 28px;
  border-radius: var(--radius-full);
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.user-name { font-size: 13px; font-weight: 500; color: var(--color-text); }
</style>
