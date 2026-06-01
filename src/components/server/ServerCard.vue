<template>
  <div class="card">
    <!-- Top: status bar -->
    <div class="card-top">
      <div class="card-status">
        <span class="status-dot" :class="`dot-${server.status}`" />
        <span class="status-label">{{ statusLabel }}</span>
      </div>
      <div class="card-actions">
        <button v-if="server.ipAddress" class="action-btn connect" @click="showTerminal = true">连接</button>
        <template v-if="server.status === 'running'">
          <button v-if="server.chargeType === 'PostPaid'" class="action-btn warn" @click="handleStop('StopCharging')">不收费</button>
          <button class="action-btn danger" @click="handleStop('KeepCharging')">停止</button>
        </template>
        <template v-if="server.status === 'stopped' || server.status === 'error'">
          <button class="action-btn primary" @click="$emit('start', server.id)">启动</button>
        </template>
        <button v-if="server.status === 'starting'" class="action-btn" disabled>启动中</button>
        <button v-if="server.status === 'stopping'" class="action-btn" disabled>停止中</button>
      </div>
    </div>

    <!-- Body: name + specs -->
    <div class="card-body">
      <div class="card-name-section">
        <div v-if="!editing" class="name-group" @click="startEdit">
          <div class="remark-line">{{ server.remark || '添加内部名称' }}</div>
          <div class="instance-line">{{ server.name }}</div>
        </div>
        <div v-else class="edit-group">
          <input v-model="editRemark" class="edit-input" @blur="saveRemark" @keydown.enter="saveRemark" @keydown.esc="cancelEdit" ref="remarkInput" placeholder="内部名称" />
          <button class="edit-check" @click="saveRemark">✓</button>
        </div>
      </div>

      <div class="card-specs">
        <div class="spec-chip">{{ server.instanceType }}</div>
        <div class="spec-chip">{{ regionName }}</div>
        <div class="spec-chip">{{ server.ipAddress || '无IP' }}</div>
        <div class="spec-chip" :class="server.chargeType === 'PostPaid' ? 'chip-postpaid' : 'chip-prepaid'">
          {{ server.chargeType === 'PostPaid' ? '按量' : '包月' }}
        </div>
      </div>

      <div class="card-resources">
        <div class="resource">
          <span class="resource-value">{{ server.spec?.cpu ?? 0 }}</span>
          <span class="resource-unit">核</span>
        </div>
        <div class="resource">
          <span class="resource-value">{{ server.spec?.memory ?? 0 }}</span>
          <span class="resource-unit">GB</span>
        </div>
        <div class="resource">
          <span class="resource-value">{{ server.spec?.disk ?? 0 }}</span>
          <span class="resource-unit">GB</span>
        </div>
        <div class="resource">
          <span class="resource-value">{{ server.spec?.bandwidth ?? 0 }}</span>
          <span class="resource-unit">Mbps</span>
        </div>
        <div class="metric">
          <div class="metric-bar"><div class="metric-fill" :class="cpu != null && cpu > 80 ? 'fill-high' : cpu != null && cpu > 50 ? 'fill-mid' : 'fill-low'" :style="{width: (cpu ?? 0)+'%'}"></div></div>
          <span class="metric-label">CPU {{ cpu ?? '--' }}{{ cpu != null ? '%' : '' }}</span>
        </div>
        <div class="metric">
          <div class="metric-bar"><div class="metric-fill" :class="mem != null && mem > 80 ? 'fill-high' : mem != null && mem > 50 ? 'fill-mid' : 'fill-low'" :style="{width: (mem ?? 0)+'%'}"></div></div>
          <span class="metric-label">内存 {{ mem ?? '--' }}{{ mem != null ? '%' : '' }}</span>
        </div>
        <div class="metric">
          <div class="metric-bar"><div class="metric-fill" :class="disk != null && disk > 80 ? 'fill-high' : disk != null && disk > 50 ? 'fill-mid' : 'fill-low'" :style="{width: (disk ?? 0)+'%'}"></div></div>
          <span class="metric-label">磁盘 {{ disk ?? '--' }}{{ disk != null ? '%' : '' }}</span>
        </div>
      </div>
    </div>

    <ConfirmDialog v-model:modelValue="stopDialogVisible" title="停止服务器"
      :message="`确定停止「${server.remark || server.name}」？`"
      type="danger" confirmText="确认停止" @confirm="handleStopConfirm" />
    <ConfirmDialog v-model:modelValue="releaseDialogVisible" title="释放服务器"
      :message="`释放后将永久删除！确定释放「${server.remark || server.name}」？`"
      type="danger" confirmText="确认释放" @confirm="handleReleaseConfirm" />
    <TerminalModal :visible="showTerminal" :server="server" @close="showTerminal = false" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Server } from '@/types'
import ServerStatus from './ServerStatus.vue'
import { ConfirmDialog } from '@/components/common'
import { updateServer } from '@/api/server'
import TerminalModal from './TerminalModal.vue'

const props = defineProps<{ server: Server }>()
const cpu = ref<number | null>(null)
const mem = ref<number | null>(null)
const disk = ref<number | null>(null)

const emit = defineEmits<{
  start: [id: string]
  stop: [id: string, mode: string]
  release: [id: string]
  namechange: [id: string, remark: string]
}>()

const stopDialogVisible = ref(false)
const releaseDialogVisible = ref(false)
const showTerminal = ref(false)
const editing = ref(false)
const editRemark = ref('')
const remarkInput = ref<HTMLInputElement>()
let pendingId = ''

function fetchMetrics() {
  const token = localStorage.getItem('token')
  fetch(`/api/servers/${props.server.id}/metrics`, {
    headers: { Authorization: `Bearer ${token}` }
  }).then(r => r.json()).then(d => {
    console.log('[Metrics]', d)
    if (d.data) {
      if (d.data.cpu != null) cpu.value = d.data.cpu
      if (d.data.memory != null) mem.value = d.data.memory
      if (d.data.disk != null) disk.value = d.data.disk
    }
  }).catch(e => console.error('[Metrics] error', e))
}
fetchMetrics()
let pendingMode = 'KeepCharging'

const regionNames: Record<string, string> = {
  'cn-hangzhou': '杭州', 'cn-shanghai': '上海', 'cn-qingdao': '青岛',
  'cn-beijing': '北京', 'cn-zhangjiakou': '张家口', 'cn-shenzhen': '深圳',
  'cn-hongkong': '香港', 'ap-southeast-1': '新加坡', 'ap-northeast-1': '东京',
  'us-west-1': '硅谷',
}
const regionName = computed(() => regionNames[props.server.region] || props.server.region)
const statusLabel = computed(() => ({
  running: '运行中', stopped: '已停止', starting: '启动中',
  stopping: '停止中', pending: '待处理', error: '异常',
}[props.server.status] || props.server.status))

function startEdit() {
  editRemark.value = props.server.remark || ''
  editing.value = true
  nextTick(() => remarkInput.value?.focus())
}
async function saveRemark() {
  const r = editRemark.value.trim()
  if (r !== (props.server.remark || '')) {
    try { await updateServer(props.server.id, { remark: r }); emit('namechange', props.server.id, r) } catch {}
  }
  editing.value = false
}
function cancelEdit() { editing.value = false }
function handleStop(mode: string) { pendingId = props.server.id; pendingMode = mode; stopDialogVisible.value = true }
function handleStopConfirm() { stopDialogVisible.value = false; emit('stop', pendingId, pendingMode) }
function handleRelease() { pendingId = props.server.id; releaseDialogVisible.value = true }
function handleReleaseConfirm() { releaseDialogVisible.value = false; emit('release', pendingId) }
</script>

<style scoped lang="scss">
.card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  margin-bottom: 14px;
  overflow: hidden;
  transition: all var(--transition);
  animation: card-in 0.3s ease both;
  animation-delay: calc(var(--i, 0) * 0.06s);
  &:hover { box-shadow: var(--shadow-md); }
}

@keyframes card-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ---- Top bar ---- */
.card-top {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 18px;
  border-bottom: 1px solid var(--color-border-light);
  gap: 12px;
}

.card-status { display: flex; align-items: center; gap: 6px; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; }
.dot-running { background: #34C759; box-shadow: 0 0 6px rgba(52,199,89,0.4); }
.dot-stopped { background: #AEAEB2; }
.dot-starting, .dot-stopping { background: #FF9F0A; }
.dot-error { background: #FF3B30; }
.status-label { font-size: 13px; font-weight: 500; color: var(--color-text-secondary); }

.card-actions { display: flex; gap: 6px; }

.action-btn {
  padding: 5px 14px; border-radius: var(--radius-full);
  border: 1px solid var(--color-border);
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  font-size: 12px; font-weight: 500; cursor: pointer;
  font-family: inherit; transition: all var(--transition);
  &:hover { background: var(--color-bg-hover); }
  &:disabled { opacity: 0.4; cursor: not-allowed; }
}
.action-btn.primary { background: #007AFF; color: white; border-color: #007AFF; &:hover { background: #0066D6; } }
.action-btn.danger { background: #FF3B30; color: white; border-color: #FF3B30; &:hover { opacity: 0.85; } }
.action-btn.warn { background: transparent; color: #D97706; border-color: #D97706; &:hover { background: #D97706; color: white; } }
.action-btn.danger-outline { background: transparent; color: #DC2626; border-color: #DC2626; &:hover { background: #DC2626; color: white; } }
.action-btn.connect { color: var(--color-primary); border-color: var(--color-primary); &:hover { background: var(--color-primary); color: white; } }

/* ---- Body ---- */
.card-body { padding: 16px 18px; }

.card-name-section { margin-bottom: 14px; }

.remark-line {
  font-size: 17px; font-weight: 700; color: var(--color-text);
  cursor: pointer; letter-spacing: -0.2px; margin-bottom: 2px;
  &:hover { color: var(--color-primary); }
}
.instance-line {
  font-size: 12px; color: var(--color-text-muted);
}
.edit-group { display: flex; align-items: center; gap: 6px; }
.edit-input {
  font-size: 15px; font-weight: 600; padding: 4px 10px;
  border: 1.5px solid var(--color-primary); border-radius: var(--radius-sm);
  outline: none; background: var(--color-bg-card); color: var(--color-text);
  font-family: inherit; width: 200px;
}
.edit-check {
  width: 24px; height: 24px; border: none; border-radius: 50%;
  background: var(--color-primary); color: white; font-size: 12px; cursor: pointer;
}

.card-specs { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
.spec-chip {
  padding: 3px 10px; border-radius: var(--radius-full);
  background: var(--color-bg); font-size: 11px; font-weight: 500;
  color: var(--color-text-secondary); white-space: nowrap;
}
.chip-postpaid { background: #EBF5FF; color: #007AFF; }
.chip-prepaid { background: #F5F5F7; color: #8B8B93; }
html.dark .chip-postpaid { background: #1A2A3A; color: #60A5FA; }
html.dark .chip-prepaid { background: #2C2C2E; color: #AEAEB2; }

.card-resources { display: flex; gap: 20px; }
.resource { display: flex; align-items: baseline; gap: 2px; }
.resource-value { font-size: 16px; font-weight: 700; color: var(--color-text); }
.resource-unit { font-size: 12px; color: var(--color-text-muted); }
.metric { min-width: 100px; }
.metric-bar { height: 4px; background: var(--color-border); border-radius: 2px; overflow: hidden; margin-bottom: 2px; }
.metric-fill { height: 100%; border-radius: 2px; transition: width 0.5s ease; }
.fill-low { background: #34C759; }
.fill-mid { background: #FF9F0A; }
.fill-high { background: #FF3B30; }
.metric-label { font-size: 11px; color: var(--color-text-muted); }
</style>
