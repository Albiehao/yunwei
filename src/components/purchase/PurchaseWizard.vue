<template>
  <div class="purchase-wizard">
    <el-steps :active="activeStep" finish-status="success" class="wizard-steps">
      <el-step title="选择配置" />
      <el-step title="确认订单" />
      <el-step title="完成购买" />
    </el-steps>

    <!-- Step 1: 选择配置 -->
    <div v-if="activeStep === 0" class="step-content">
      <h3>选择实例规格</h3>
      <el-row :gutter="16">
        <el-col :span="8" v-for="inst in instanceTypes" :key="inst.id">
          <InstanceTypeCard
            :instance="inst"
            :selected="selectedType === inst.id"
            @select="selectedType = inst.id"
          />
        </el-col>
      </el-row>

      <el-divider />

      <h3>配置详情</h3>
      <el-form label-width="140px" class="config-form">
        <el-form-item label="实例名称">
          <el-input v-model="form.name" placeholder="自定义实例名称" />
        </el-form-item>
        <el-form-item label="地域">
          <el-select v-model="form.region" style="width:100%">
            <el-option label="华东1（杭州）" value="cn-hangzhou" />
            <el-option label="华东2（上海）" value="cn-shanghai" />
            <el-option label="华北2（北京）" value="cn-beijing" />
            <el-option label="华南1（深圳）" value="cn-shenzhen" />
          </el-select>
        </el-form-item>
        <el-form-item label="付费方式">
          <el-radio-group v-model="form.chargeType">
            <el-radio-button value="PostPaid">按量付费</el-radio-button>
            <el-radio-button value="PrePaid">包年包月</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="form.chargeType === 'PrePaid'" label="购买时长">
          <el-select v-model="form.duration" style="width:100%">
            <el-option label="1个月" :value="1" />
            <el-option label="3个月" :value="3" />
            <el-option label="6个月" :value="6" />
            <el-option label="12个月" :value="12" />
          </el-select>
        </el-form-item>
        <el-form-item label="购买数量">
          <el-input-number v-model="form.quantity" :min="1" :max="100" />
        </el-form-item>
      </el-form>
    </div>

    <!-- Step 2: 确认订单 -->
    <div v-if="activeStep === 1" class="step-content">
      <h3>确认订单</h3>
      <el-descriptions :column="1" border class="order-summary">
        <el-descriptions-item label="实例类型">{{ selectedInstance?.name }}</el-descriptions-item>
        <el-descriptions-item label="实例名称">{{ form.name }}</el-descriptions-item>
        <el-descriptions-item label="地域">{{ form.region }}</el-descriptions-item>
        <el-descriptions-item label="配置">
          {{ selectedInstance?.cpu }} vCPU / {{ selectedInstance?.memory }}GB
        </el-descriptions-item>
        <el-descriptions-item label="付费方式">
          {{ form.chargeType === 'PostPaid' ? '按量付费' : '包年包月' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="form.chargeType === 'PrePaid'" label="购买时长">
          {{ form.duration }} 个月
        </el-descriptions-item>
        <el-descriptions-item label="购买数量">{{ form.quantity }} 台</el-descriptions-item>
        <el-descriptions-item label="费用">
          <span style="color:var(--el-color-danger);font-size:18px;font-weight:700">
            ¥ {{ totalCost.toFixed(2) }}
          </span>
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <!-- Step 3: 完成 -->
    <div v-if="activeStep === 2" class="step-content step-success">
      <el-icon :size="64" color="#67c23a"><SuccessFilled /></el-icon>
      <h3>购买成功！</h3>
      <p>服务器 <strong>{{ purchasedServer?.name }}</strong> 正在创建中...</p>
      <p class="step-hint">创建完成后可在「服务器管理」页面查看</p>
    </div>

    <!-- Buttons -->
    <div class="step-actions">
      <el-button v-if="activeStep > 0 && activeStep < 2" @click="activeStep--">
        上一步
      </el-button>
      <el-button
        v-if="activeStep < 2"
        type="primary"
        :disabled="!canNext"
        :loading="submitting"
        @click="handleNext"
      >
        {{ activeStep === 0 ? '下一步' : '确认购买' }}
      </el-button>
      <el-button v-if="activeStep === 2" type="primary" @click="$emit('done')">
        返回控制台
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { InstanceType, Server, PurchaseParams } from '@/types'
import { getInstanceTypes, purchaseServer } from '@/api/purchase'
import InstanceTypeCard from './InstanceTypeCard.vue'

const emit = defineEmits<{
  done: []
}>()

const activeStep = ref(0)
const instanceTypes = ref<InstanceType[]>([])
const selectedType = ref('')
const submitting = ref(false)
const purchasedServer = ref<Server | null>(null)

const form = ref<PurchaseParams>({
  instanceType: '',
  region: 'cn-hangzhou',
  name: '',
  chargeType: 'PostPaid',
  quantity: 1
})

const selectedInstance = computed(() =>
  instanceTypes.value.find(i => i.id === selectedType.value)
)

const totalCost = computed(() => {
  const inst = selectedInstance.value
  if (!inst) return 0
  if (form.value.chargeType === 'PostPaid') {
    return inst.hourlyPrice * form.value.quantity
  }
  return (inst.monthlyPrice || inst.hourlyPrice * 24 * 30) * (form.value.duration || 1) * form.value.quantity
})

const canNext = computed(() => {
  if (activeStep.value === 0) {
    return selectedType.value && form.value.name && form.value.region
  }
  return true
})

async function handleNext() {
  if (activeStep.value === 1) {
    // Submit purchase
    submitting.value = true
    form.value.instanceType = selectedType.value
    try {
      const res = await purchaseServer(form.value)
      purchasedServer.value = res.data
      activeStep.value++
    } catch (e) {
      console.error('Purchase failed', e)
    } finally {
      submitting.value = false
    }
  } else {
    activeStep.value++
  }
}

onMounted(async () => {
  try {
    const res = await getInstanceTypes()
    instanceTypes.value = res.data
    if (res.data.length > 0) {
      selectedType.value = res.data[0].id
    }
  } catch (e) {
    console.error('Failed to load instance types', e)
  }
})
</script>

<style scoped lang="scss">
.purchase-wizard {
  max-width: 960px;
  margin: 0 auto;
}
.wizard-steps {
  margin-bottom: 32px;
}
.step-content {
  min-height: 300px;
  h3 {
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 16px;
  }
}
.config-form {
  max-width: 600px;
}
.step-success {
  text-align: center;
  padding: 40px 0;
  h3 {
    margin-top: 16px;
    font-size: 20px;
  }
}
.step-hint {
  font-size: 13px;
  color: var(--el-text-color-secondary);
}
.step-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--el-border-color-light);
}
.order-summary {
  max-width: 600px;
  margin: 0 auto;
}
</style>
