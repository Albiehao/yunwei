<template>
  <div class="user-list-page">
    <PageHeader title="用户管理" description="管理系统用户账号与权限">
      <template #actions>
        <Button variant="primary" @click="openCreate">添加用户</Button>
      </template>
    </PageHeader>

    <!-- Loading -->
    <template v-if="userStore.loading && userStore.users.length === 0">
      <div v-for="i in 3" :key="i" class="card-loading">
        <SkeletonLoader :count="2" />
      </div>
    </template>

    <!-- Error -->
    <Alert v-else-if="errorMessage" type="danger">
      {{ errorMessage }}
      <template #action>
        <Button variant="danger" size="sm" @click="loadUsers">重试</Button>
      </template>
    </Alert>

    <!-- Table -->
    <div v-else class="table-wrapper">
      <Table :columns="columns" :data="userStore.users">
        <template #cell-role="{ row }">
          <Badge :variant="roleBadgeType(row.role)">{{ roleLabel(row.role) }}</Badge>
        </template>
        <template #cell-status="{ row }">
          <Badge :variant="row.status === 'active' ? 'success' : 'default'">
            {{ row.status === 'active' ? '启用' : '停用' }}
          </Badge>
        </template>
        <template #cell-actions="{ row }">
          <div class="action-btns">
            <Button size="sm" variant="secondary" @click="openEdit(row)">编辑</Button>
            <Button size="sm" variant="danger" @click="handleDelete(row)">删除</Button>
          </div>
        </template>
      </Table>
    </div>

    <!-- Empty -->
    <EmptyState v-if="!userStore.loading && userStore.users.length === 0" description="暂无用户" />

    <!-- Create/Edit Modal -->
    <Modal v-if="showModal" :title="isEditing ? '编辑用户' : '添加用户'" @close="closeModal">
      <div class="modal-form">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <Input v-model="editForm.username" placeholder="请输入用户名" />
        </div>
        <div class="form-group">
          <label class="form-label">邮箱</label>
          <Input v-model="editForm.email" placeholder="请输入邮箱" />
        </div>
        <div class="form-group">
          <label class="form-label">手机号</label>
          <Input v-model="editForm.phone" placeholder="请输入手机号" />
        </div>
        <div class="form-group">
          <label class="form-label">角色</label>
          <Select v-model="editForm.role" :options="roleOptions" />
        </div>
        <div class="form-group">
          <label class="form-label">状态</label>
          <Select v-model="editForm.status" :options="statusOptions" />
        </div>
      </div>
      <template #footer>
        <Button variant="secondary" @click="closeModal">取消</Button>
        <Button variant="primary" :loading="saving" @click="save">{{ isEditing ? '保存' : '创建' }}</Button>
      </template>
    </Modal>

    <!-- Delete Confirm -->
    <ConfirmDialog
      v-if="deleteTarget"
      title="确认删除"
      :message="`确定要删除用户 ${deleteTarget.username} 吗？此操作不可恢复。`"
      @confirm="confirmDelete"
      @cancel="deleteTarget = null"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores'
import { PageHeader, EmptyState, SkeletonLoader, ConfirmDialog } from '@/components/common'
import { Button, Input, Select, Table, Badge, Modal, Alert } from '@/components/ui'
import type { User } from '@/types/common'

const userStore = useUserStore()

const errorMessage = ref('')
const showModal = ref(false)
const isEditing = ref(false)
const saving = ref(false)
const deleteTarget = ref<User | null>(null)
const editForm = reactive({
  username: '',
  email: '',
  phone: '',
  role: 'developer' as string,
  status: 'active' as string
})
let editingId = ''

const columns = [
  { key: 'username', label: '用户名' },
  { key: 'email', label: '邮箱' },
  { key: 'phone', label: '手机号' },
  { key: 'role', label: '角色' },
  { key: 'status', label: '状态' },
  { key: 'createdAt', label: '创建时间' },
  { key: 'actions', label: '操作' }
]

const roleOptions = [
  { label: '管理员', value: 'admin' },
  { label: '运维', value: 'operator' },
  { label: '开发', value: 'developer' },
  { label: '审计', value: 'auditor' }
]

const statusOptions = [
  { label: '启用', value: 'active' },
  { label: '停用', value: 'disabled' }
]

function roleLabel(role: string) {
  const map: Record<string, string> = { admin: '管理员', operator: '运维', developer: '开发', auditor: '审计' }
  return map[role] || role
}

function roleBadgeType(role: string) {
  const map: Record<string, string> = { admin: 'danger', operator: 'primary', developer: 'success', auditor: 'warning' }
  return map[role] || 'default'
}

function openCreate() {
  isEditing.value = false
  editingId = ''
  editForm.username = ''
  editForm.email = ''
  editForm.phone = ''
  editForm.role = 'developer'
  editForm.status = 'active'
  showModal.value = true
}

function openEdit(user: User) {
  isEditing.value = true
  editingId = user.id
  editForm.username = user.username
  editForm.email = user.email
  editForm.phone = user.phone || ''
  editForm.role = user.role
  editForm.status = user.status
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function save() {
  saving.value = true
  try {
    if (isEditing.value) {
      await userStore.editUser(editingId, { ...editForm } as any)
    } else {
      await userStore.addUser({ ...editForm } as any)
    }
    closeModal()
  } catch (e: any) {
    errorMessage.value = e.response?.data?.message || '操作失败'
  } finally {
    saving.value = false
  }
}

function handleDelete(user: User) {
  deleteTarget.value = user
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  try {
    await userStore.removeUser(deleteTarget.value.id)
  } catch (e: any) {
    errorMessage.value = e.response?.data?.message || '删除失败'
  }
  deleteTarget.value = null
}

async function loadUsers() {
  errorMessage.value = ''
  await userStore.fetchUsers()
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped lang="scss">
.table-wrapper {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.card-loading {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 16px;
}

.action-btns {
  display: flex;
  gap: 8px;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 8px 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
}
</style>
