<template>
  <div class="purchase-page">
    <PageHeader title="购买服务器" description="选择配置并创建新的云服务器实例" />
    <PurchaseWizard @done="handleDone" />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { PageHeader } from '@/components/common'
import { PurchaseWizard } from '@/components/purchase'

const router = useRouter()

function handleDone() {
  router.push('/servers')
}
</script>

<style scoped lang="scss">
.purchase-page {
  max-width: 1000px;
}
</style>
