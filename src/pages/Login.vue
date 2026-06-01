<template>
  <div class="login-page">
    <div class="login-bg" />
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <svg width="40" height="40" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="8" fill="var(--color-primary)"/>
            <path d="M16 8l8 4.5v7L16 24l-8-4.5v-7L16 8z" stroke="white" stroke-width="1.5" fill="none"/>
            <path d="M16 13l3 2v3l-3 2-3-2v-3l3-2z" stroke="white" stroke-width="1.5" fill="none"/>
          </svg>
        </div>
        <h1 class="title">寻天运维平台</h1>
        <p class="subtitle">登录以管理你的云服务器</p>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <Input v-model="form.username" placeholder="请输入用户名" prefix-icon="user" />
        </div>
        <div class="form-group">
          <label class="form-label">密码</label>
          <Input v-model="form.password" type="password" placeholder="请输入密码" prefix-icon="lock" />
        </div>

        <Alert v-if="errorMessage" type="danger" style="margin-bottom:2px">
          {{ errorMessage }}
        </Alert>

        <Button type="submit" variant="primary" :loading="loading" style="width:100%;padding:12px;font-size:15px;margin-top:4px">
          {{ loading ? '登录中...' : '登录' }}
        </Button>

      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores'
import { Button, Input, Alert } from '@/components/ui'

const router = useRouter()
const userStore = useUserStore()
const form = reactive({ username: '', password: '' })
const loading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  if (!form.username || !form.password) {
    errorMessage.value = '请输入用户名和密码'
    return
  }
  loading.value = true
  errorMessage.value = ''
  try {
    await userStore.login(form.username, form.password)
    router.push('/servers')
  } catch {
    errorMessage.value = '用户名或密码错误'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.login-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 40%, #f093fb 70%, #f5576c 100%);
  background-size: 200% 200%;
  animation: gradient-shift 8s ease infinite;
}

@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login-card {
  position: relative;
  z-index: 1;
  width: 400px;
  max-width: 90%;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(40px);
  -webkit-backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: var(--radius-2xl);
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.login-header { text-align: center; margin-bottom: 32px; }
.logo { display: flex; justify-content: center; margin-bottom: 16px; }

.title {
  font-size: 24px; font-weight: 700;
  color: white;
  margin: 0 0 4px;
  letter-spacing: -0.3px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

.login-form { display: flex; flex-direction: column; gap: 14px; }

.form-group { display: flex; flex-direction: column; gap: 5px; }

.form-label {
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
}

</style>
