import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)

  // Dark mode with localStorage persistence
  const isDark = ref(localStorage.getItem('theme') === 'dark')

  function toggleDark() {
    isDark.value = !isDark.value
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
    applyTheme()
  }

  function applyTheme() {
    const html = document.documentElement
    if (isDark.value) {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }
  }

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  // Initialize theme on creation
  if (typeof document !== 'undefined') {
    applyTheme()
  }

  return {
    sidebarCollapsed,
    isDark,
    toggleSidebar,
    toggleDark,
    applyTheme
  }
})
