<template>
  <Teleport to="body">
  <div v-if="visible" class="overlay" @click.self="close">
    <div class="box">
      <div class="box-hd">
        <span>{{ title }}</span>
        <button class="box-x" @click="close">✕</button>
      </div>

      <div v-if="!sshId" class="login">
        <div class="f"><label>主机</label><input v-model="h" class="i" readonly /></div>
        <div class="f"><label>用户</label><input v-model="u" class="i" style="max-width:80px" /></div>
        <div class="f"><label>密码</label><input v-model="pw" type="password" class="i" @keydown.enter="doConn" /></div>
        <div class="f"><label>端口</label><input v-model="po" class="i" style="max-width:60px" /></div>
        <div class="f" style="justify-content:flex-end;gap:8px">
          <button class="b" @click="doConn" :disabled="loading">{{ loading ? '连接中...' : '连接' }}</button>
        </div>
        <div v-if="err" class="e">{{ err }}</div>
      </div>

      <div v-else class="term-wrap">
        <div class="term-out">
          <textarea ref="outRef" readonly :value="log" class="term-text" @scroll="onScroll"></textarea>
        </div>
        <div class="term-inp">
          <span class="prompt">$</span>
          <input ref="inpRef" v-model="cmd" class="ci" @keydown.enter="doExec" placeholder="输入命令" />
          <button class="b b-sm" @click="doExec">执行</button>
          <button class="b b-outline" @click="doDisconn">断开</button>
        </div>
      </div>
    </div>
  </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onUnmounted } from 'vue'
import type { Server } from '@/types'

const props = withDefaults(defineProps<{ visible: boolean; server?: Server | null }>(), { visible: false, server: null })
const emit = defineEmits<{ close: [] }>()
const outRef = ref<HTMLTextAreaElement>()
const inpRef = ref<HTMLInputElement>()
const log = ref('')
const cmd = ref('')
const h = ref('')
const u = ref('root')
const pw = ref('')
const po = ref('22')
const sshId = ref('')
const loading = ref(false)
const err = ref('')
const title = ref('SSH')
const autoScroll = ref(true)

watch(() => props.visible, (v) => {
  if (!v || !props.server) return
  h.value = props.server.ipAddress || ''
  u.value = 'root'; pw.value = ''; po.value = '22'
  sshId.value = ''; loading.value = false; err.value = ''
  log.value = ''; title.value = props.server.remark || props.server.name
})

function scrollDown() { nextTick(() => { if (outRef.value && autoScroll.value) outRef.value.scrollTop = outRef.value.scrollHeight }) }
function onScroll() { if (!outRef.value) return; autoScroll.value = outRef.value.scrollTop + outRef.value.clientHeight >= outRef.value.scrollHeight - 20 }

function write(s: string) { log.value += s; scrollDown() }

async function doConn() {
  if (!h.value) { err.value = '主机为空'; return }
  loading.value = true; err.value = ''
  try {
    const token = localStorage.getItem('token')
    const r = await fetch('/api/ssh/connect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ host: h.value, username: u.value, password: pw.value, port: parseInt(po.value) || 22 })
    })
    const d = await r.json()
    if (d.code !== 200) { err.value = d.message; loading.value = false; return }
    sshId.value = d.data.id
    title.value = `${u.value}@${h.value}`
    write(`已连接 ${u.value}@${h.value}\n`)
    loading.value = false
    nextTick(() => inpRef.value?.focus())
  } catch (e: any) { err.value = `请求失败: ${e.message}`; loading.value = false }
}

async function doExec() {
  if (!cmd.value || !sshId.value) return
  const c = cmd.value
  write(`$ ${c}\n`)
  cmd.value = ''
  try {
    const token = localStorage.getItem('token')
    const r = await fetch('/api/ssh/exec', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ id: sshId.value, command: c })
    })
    const d = await r.json()
    if (d.code === 200 && d.data) {
      write(d.data.output || '')
      if (d.data.exit_code !== 0) write(`\n[退出码: ${d.data.exit_code}]\n`)
    } else { write(`错误: ${d.message}\n`) }
  } catch (e: any) { write(`请求失败: ${e.message}\n`) }
}

async function doDisconn() {
  if (sshId.value) {
    try {
      const token = localStorage.getItem('token')
      await fetch('/api/ssh/disconnect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ id: sshId.value })
      })
    } catch {}
  }
  sshId.value = ''; write('已断开\n')
}

function close() { if (sshId.value) doDisconn(); emit('close') }
onUnmounted(() => { if (sshId.value) doDisconn() })
</script>

<style scoped lang="scss">
.overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.25); backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center; z-index: 2000; padding: 20px;
}
.box {
  width: 800px; max-width: 100%; height: 500px; max-height: 100%;
  display: flex; flex-direction: column;
  background: var(--color-bg-card); border: 1px solid var(--color-border);
  border-radius: 14px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.12);
}
.box-hd {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 16px; border-bottom: 1px solid var(--color-border);
  font-size: 14px; font-weight: 600; flex-shrink: 0;
}
.box-x {
  width: 28px; height: 28px; border: none; background: transparent; border-radius: 50%;
  cursor: pointer; font-size: 16px; color: var(--color-text-muted);
  display: flex; align-items: center; justify-content: center;
  &:hover { background: var(--color-bg-hover); color: var(--color-text); }
}

.login {
  flex: 1; display: flex; flex-direction: column; justify-content: center;
  padding: 24px 32px; gap: 12px; max-width: 400px; margin: 0 auto; width: 100%;
}
.f { display: flex; align-items: center; gap: 10px; }
.f label { width: 35px; font-size: 13px; color: var(--color-text-secondary); }
.i {
  flex: 1; padding: 7px 10px; border: 1px solid var(--color-border); border-radius: 6px;
  background: var(--color-bg); color: var(--color-text); font-size: 13px; outline: none;
  &:focus { border-color: var(--color-primary); }
  &[readonly] { opacity: 0.5; }
}
.b {
  padding: 7px 24px; border: none; border-radius: 6px; background: var(--color-primary);
  color: white; font-size: 13px; font-weight: 600; cursor: pointer;
  &:disabled { opacity: 0.5; }
}
.b-outline { background: transparent; color: var(--color-danger); border: 1px solid var(--color-danger); padding: 6px 16px; }
.b-sm { padding: 6px 16px; }
.e { color: var(--color-danger); font-size: 13px; text-align: center; }

.term-wrap { flex: 1; display: flex; flex-direction: column; min-height: 0; }
.term-out { flex: 1; background: #0d1117; min-height: 0; }
.term-text {
  width: 100%; height: 100%; padding: 10px 12px; resize: none; border: none; outline: none;
  background: transparent; color: #e6edf3; font-family: 'JetBrains Mono', monospace;
  font-size: 13px; line-height: 1.5; tab-size: 4;
}
.term-inp {
  display: flex; align-items: center; gap: 6px;
  padding: 8px 12px; border-top: 1px solid var(--color-border);
  background: var(--color-bg-card);
}
.prompt { font-family: monospace; font-size: 13px; color: var(--color-text-muted); }
.ci {
  flex: 1; padding: 6px 10px; border: 1px solid var(--color-border); border-radius: 6px;
  background: var(--color-bg); color: var(--color-text); font-size: 13px; font-family: inherit; outline: none;
  &:focus { border-color: var(--color-primary); }
}
</style>
