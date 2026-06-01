<template>
  <div class="page">
    <PageHeader title="操作日志" />

    <div class="filter-bar">
      <select v-model="actionFilter" class="fi" @change="load">
        <option value="">全部操作</option>
        <option value="start">启动</option>
        <option value="stop">停止</option>
        <option value="release">释放</option>
        <option value="exec_ssh">SSH</option>
        <option value="schedule">定时任务</option>
      </select>
      <button class="btn" @click="load">刷新</button>
    </div>

    <div v-if="loading" class="loading"><SkeletonLoader :count="5" /></div>
    <div v-else-if="items.length === 0"><EmptyState description="暂无日志" /></div>
    <div v-else class="table-wrap">
      <table class="table">
        <thead><tr>
          <th>时间</th><th>用户</th><th>操作</th><th>详情</th><th>结果</th>
        </tr></thead>
        <tbody>
          <tr v-for="log in items" :key="log.id">
            <td class="cell-time">{{ fmt(log.createdAt) }}</td>
            <td>{{ log.username }}</td>
            <td><span class="tag" :class="'tag-'+actionClass(log.action)">{{ actionLabel(log.action) }}</span></td>
            <td class="cell-detail">{{ log.detail || '-' }}</td>
            <td><span class="tag" :class="log.result === 'success' ? 'tag-ok' : 'tag-fail'">{{ log.result === 'success' ? '成功' : '失败' }}</span></td>
          </tr>
        </tbody>
      </table>
      <div v-if="total > pageSize" class="pager">
        <button class="btn btn-sm" :disabled="page <= 1" @click="page--; load()">上一页</button>
        <span class="pi">{{ page }}/{{ Math.ceil(total / pageSize) }}</span>
        <button class="btn btn-sm" :disabled="page * pageSize >= total" @click="page++; load()">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { PageHeader, EmptyState, SkeletonLoader } from '@/components/common'

const items = ref<any[]>([])
const loading = ref(false)
const page = ref(1)
const total = ref(0)
const pageSize = ref(50)
const actionFilter = ref('')

function actionLabel(a: string) { return { start:'启动', stop:'停止', release:'释放', exec_ssh:'SSH', schedule:'定时任务' }[a] || a }
function actionClass(a: string) { return { start:'ok', stop:'fail', release:'fail', exec_ssh:'info', schedule:'warn' }[a] || 'info' }
function fmt(iso: string) { return iso ? iso.slice(0,19).replace('T',' ') : '-' }

async function load() {
  loading.value = true
  try {
    const t = localStorage.getItem('token')
    const url = `/api/logs?page=${page.value}&pageSize=${pageSize.value}${actionFilter.value ? '&action='+actionFilter.value : ''}`
    const r = await fetch(url, { headers: { Authorization: `Bearer ${t}` } })
    const d = await r.json()
    if (d.data) { items.value = d.data.items; total.value = d.data.total }
  } catch {}
  loading.value = false
}

onMounted(load)
</script>

<style scoped lang="scss">
.filter-bar { display:flex; gap:8px; align-items:center; margin-bottom:16px; background:var(--color-bg-card); border:1px solid var(--color-border); border-radius:8px; padding:12px 16px; }
.fi { padding:6px 10px; border:1px solid var(--color-border); border-radius:6px; background:var(--color-bg-card); color:var(--color-text); font-size:13px; outline:none; }
.btn { padding:6px 16px; border:none; border-radius:6px; background:var(--color-primary); color:white; font-size:12px; cursor:pointer; }
.btn-sm { padding:4px 12px; font-size:12px; }
.btn:disabled { opacity:0.5; }
.loading { padding:20px; background:var(--color-bg-card); border-radius:8px; }
.table-wrap { background:var(--color-bg-card); border:1px solid var(--color-border); border-radius:8px; overflow:hidden; }
.table { width:100%; border-collapse:collapse; font-size:13px; }
th { text-align:left; padding:10px 14px; font-weight:600; font-size:12px; color:var(--color-text-muted); background:var(--color-bg); border-bottom:1px solid var(--color-border); }
td { padding:9px 14px; border-bottom:1px solid var(--color-border-light); }
tbody tr:hover { background:var(--color-bg-hover); }
.cell-time { white-space:nowrap; font-family:monospace; font-size:12px; }
.cell-detail { max-width:300px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.tag { padding:2px 8px; border-radius:4px; font-size:12px; font-weight:500; }
.tag-ok { background:#EBFFF2; color:#34C759; }
.tag-fail { background:#FFF0EF; color:#FF3B30; }
.tag-info { background:#EBF5FF; color:#007AFF; }
.tag-warn { background:#FFF8EB; color:#FF9F0A; }
.pager { display:flex; align-items:center; justify-content:center; gap:12px; padding:10px; border-top:1px solid var(--color-border); }
.pi { font-size:13px; color:var(--color-text-secondary); }
</style>
