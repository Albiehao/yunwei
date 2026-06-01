import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as loginApi, getMe } from '@/api/auth'
import { getUsers, createUser, updateUser, deleteUser } from '@/api/user'
import type { User } from '@/types/common'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<User | null>(null)
  const token = ref(localStorage.getItem('token') || '')
  const users = ref<User[]>([])
  const loading = ref(false)

  async function login(username: string, password: string) {
    const res = await loginApi({ username, password })
    token.value = res.data.token
    currentUser.value = res.data.user as any
    localStorage.setItem('token', res.data.token)
    return res.data
  }

  function logout() {
    token.value = ''
    currentUser.value = null
    localStorage.removeItem('token')
  }

  async function fetchUsers() {
    loading.value = true
    try {
      const res = await getUsers()
      users.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function addUser(data: Partial<User>) {
    const res = await createUser(data)
    users.value.push(res.data)
  }

  async function editUser(id: string, data: Partial<User>) {
    const res = await updateUser(id, data)
    const idx = users.value.findIndex(u => u.id === id)
    if (idx !== -1) users.value[idx] = res.data
  }

  async function removeUser(id: string) {
    await deleteUser(id)
    users.value = users.value.filter(u => u.id !== id)
  }

  return { currentUser, token, users, loading, login, logout, fetchUsers, addUser, editUser, removeUser }
})
