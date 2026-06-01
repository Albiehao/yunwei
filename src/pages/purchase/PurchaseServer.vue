<template>
  <div class="page">
    <PageHeader title="购买服务器" />

    <template v-if="loading"><SkeletonLoader :count="5" /></template>

    <div v-else class="layout">
      <!-- Left: Spec selector -->
      <div class="left">
        <div class="panel-title">选择规格</div>
        <div class="spec-list">
          <div v-for="t in types" :key="t.id" class="spec" :class="{ on: selected === t.id }" @click="pick(t.id)">
            <div class="spec-top">
              <span class="spec-name">{{ t.id }}</span>
              <span class="spec-price">{{ selPrice != null ? '¥' + selPrice : '' }}</span>
            </div>
            <div class="spec-specs">{{ t.cpu }}核 · {{ t.memory }}GB · {{ t.family }}</div>
          </div>
        </div>
      </div>

      <!-- Right: Config form -->
      <div class="right">
        <div class="panel-title">配置</div>

        <div class="cfg">
          <div class="cfg-row">
            <label>名称</label>
            <input v-model="form.name" class="ci" placeholder="my-server" />
          </div>
          <div class="cfg-row">
            <label>地域</label>
            <select v-model="form.region" class="ci" @change="onRegionChange">
              <option v-for="r in regions" :key="r.v" :value="r.v">{{ r.l }}</option>
            </select>
          </div>
          <div class="cfg-row">
            <label>镜像</label>
            <select v-model="form.imageId" class="ci">
              <option v-for="img in images" :key="img.id" :value="img.id">{{ img.osName || img.name }}</option>
            </select>
          </div>
          <div class="cfg-row">
            <label>系统盘</label>
            <select v-model="form.diskSize" class="ci ci-s">
              <option v-for="s in [20,40,60,80,100,120]" :key="s" :value="s">{{ s }}GB</option>
            </select>
          </div>
          <div class="cfg-row">
            <label>带宽</label>
            <select v-model="form.bandwidth" class="ci ci-s"><option v-for="b in [1,5,10,20,50,100,200]" :key="b" :value="b">{{ b }}Mbps</option></select>
            <select v-model="form.billingMode" class="ci ci-m">
              <option value="PayByBandwidth">固定带宽</option>
              <option value="PayByTraffic">按流量</option>
            </select>
          </div>
          <div class="cfg-row">
            <label>密码</label>
            <input v-model="form.password" type="password" class="ci" placeholder="实例密码" />
          </div>
          <div class="cfg-row">
            <label>数量</label>
            <input v-model.number="form.quantity" type="number" class="ci ci-s" min="1" max="10" @input="calcTotal" />
            <span class="qty-label">台</span>
          </div>
        </div>

        <!-- Price summary -->
        <div class="summary">
          <div class="sum-row"><span>规格单价</span><span>{{ selPrice != null ? '¥' + selPrice + '/时' : '--' }}</span></div>
          <div class="sum-row"><span>数量</span><span>{{ form.quantity }} 台</span></div>
          <div class="sum-row total"><span>预估每小时</span><span>{{ totalPrice != null ? '¥' + totalPrice.toFixed(4) : '--' }}</span></div>
        </div>

        <div class="bottom">
          <button class="btn-buy" @click="submit" :disabled="buying">{{ buying ? '提交中...' : '提交采购' }}</button>
          <span v-if="msg" class="msg">{{ msg }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { PageHeader, SkeletonLoader } from '@/components/common'

const router = useRouter()
const types = ref<any[]>([])
const images = ref<any[]>([])
const groups = ref<any[]>([])
const vs = ref<any[]>([])
const selected = ref('')
const selPrice = ref<number | null>(null)
const totalPrice = ref<number | null>(null)
const loading = ref(false)
const buying = ref(false)
const msg = ref('')

const form = reactive({
  name: '', region: 'cn-hongkong', imageId: '',
  diskSize: 40, bandwidth: 100, billingMode: 'PayByBandwidth',
  password: '', quantity: 1, sgId: '', vswId: '',
})

const regions = [
  { v: 'cn-hongkong', l: '香港' }, { v: 'cn-hangzhou', l: '杭州' },
  { v: 'cn-shanghai', l: '上海' }, { v: 'cn-beijing', l: '北京' },
  { v: 'cn-shenzhen', l: '深圳' }, { v: 'ap-southeast-1', l: '新加坡' },
]

function calcTotal() {
  if (selPrice.value != null) totalPrice.value = selPrice.value * form.quantity
  else totalPrice.value = null
}

async function pick(id: string) {
  selected.value = id; selPrice.value = null; totalPrice.value = null
  try {
    const t = localStorage.getItem('token')
    const r = await fetch(`/api/servers/price?instanceType=${id}&region=${form.region}`, { headers: { Authorization: `Bearer ${t}` } })
    const d = await r.json()
    if (d.data?.price != null) { selPrice.value = d.data.price; calcTotal() } else if (d.data?.hourly != null) { selPrice.value = d.data.hourly; calcTotal() }
  } catch {}
}

async function load() {
  loading.value = true
  try {
    const t = localStorage.getItem('token')
    const h = { Authorization: `Bearer ${t}` }
    const [r1, r2] = await Promise.all([
      fetch('/api/servers/instance-types', { headers: h }).then(r => r.json()),
      fetch(`/api/servers/resources?region=${form.region}`, { headers: h }).then(r => r.json()),
    ])
    if (r1.data) types.value = r1.data
    if (r2.data) { images.value = r2.data.images || []; groups.value = r2.data.securityGroups || []; vs.value = r2.data.vswitches || [] }
    if (types.value.length) pick(types.value[0].id)
  } catch {}
  loading.value = false
}

async function onRegionChange() {
  const t = localStorage.getItem('token')
  const r = await fetch(`/api/servers/resources?region=${form.region}`, { headers: { Authorization: `Bearer ${t}` } })
  const d = await r.json()
  if (d.data) { images.value = d.data.images || []; groups.value = d.data.securityGroups || []; vs.value = d.data.vswitches || [] }
}

async function submit() {
  if (!selected.value || !form.name) return
  buying.value = true
  try {
    const t = localStorage.getItem('token')
    await fetch('/api/tasks', {
      method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${t}` },
      body: JSON.stringify({ action: 'purchase', serverId: '', ...form, instanceType: selected.value })
    })
    msg.value = '采购请求已提交'
    setTimeout(() => router.push('/tasks'), 1200)
  } catch { msg.value = '提交失败' }
  buying.value = false
}

onMounted(load)
</script>

<style scoped lang="scss">
.layout { display: flex; gap: 24px; align-items: flex-start; }
.left { flex: 1; min-width: 0; }
.right { width: 380px; flex-shrink: 0; position: sticky; top: 24px; align-self: flex-start; }

.panel-title { font-size: 15px; font-weight: 600; margin-bottom: 12px; }

.spec-list { display: flex; flex-direction: column; gap: 6px; }
.spec {
  border: 1px solid var(--color-border); border-radius: var(--radius-lg);
  padding: 12px 16px; cursor: pointer; transition: all 0.15s;
  &:hover { border-color: var(--color-primary-light); }
  &.on { border-color: var(--color-primary); background: var(--color-primary-bg); }
}
.spec-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.spec-name { font-size: 13px; font-weight: 600; font-family: var(--font-mono); }
.spec-price { font-size: 13px; color: var(--color-primary); font-weight: 600; }
.spec-specs { font-size: 12px; color: var(--color-text-muted); }

.cfg { display: flex; flex-direction: column; gap: 10px; }
.cfg-row { display: flex; align-items: center; gap: 8px; }
.cfg-row label { width: 48px; font-size: 13px; color: var(--color-text-secondary); flex-shrink: 0; }
.ci {
  flex: 1; padding: 7px 10px; border: 1px solid var(--color-border); border-radius: var(--radius-md);
  background: var(--color-bg-card); color: var(--color-text); font-size: 13px; outline: none;
  &:focus { border-color: var(--color-primary); }
}
.ci-s { max-width: 90px; }
.ci-m { max-width: 110px; }
.qty-label { font-size: 13px; color: var(--color-text-muted); }

.summary {
  margin-top: 16px; padding: 14px 16px;
  background: var(--color-bg); border-radius: var(--radius-lg);
}
.sum-row { display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; color: var(--color-text-secondary); }
.sum-row.total { font-size: 15px; font-weight: 700; color: var(--color-text); border-top: 1px solid var(--color-border); margin-top: 4px; padding-top: 8px; }

.bottom { display: flex; align-items: center; gap: 12px; margin-top: 16px; }
.btn-buy {
  padding: 10px 32px; border: none; border-radius: var(--radius-full);
  background: var(--color-primary); color: white; font-size: 14px; font-weight: 600; cursor: pointer;
  &:disabled { opacity: 0.5; }
}
.msg { font-size: 13px; color: var(--color-success); }
</style>
