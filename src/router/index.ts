import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/Login.vue'),
      meta: { title: '登录' }
    },
    {
      path: '/',
      component: MainLayout,
      redirect: '/servers',
      children: [
        {
          path: 'servers',
          name: 'servers',
          component: () => import('@/pages/server/ServerList.vue'),
          meta: { title: '我的服务器', icon: 'server', requiresAuth: true }
        },
        {
          path: 'schedules',
          name: 'schedules',
          component: () => import('@/pages/schedule/ScheduleList.vue'),
          meta: { title: '定时开关', icon: 'schedule', requiresAuth: true }
        },
        {
          path: 'release',
          name: 'release',
          component: () => import('@/pages/release/ReleaseList.vue'),
          meta: { title: '释放实例', icon: 'trash', requiresAuth: true }
        },
        {
          path: 'users',
          name: 'users',
          component: () => import('@/pages/user/UserList.vue'),
          meta: { title: '用户管理', icon: 'user', requiresAuth: true, role: 'admin' }
        },
        {
          path: 'logs',
          name: 'logs',
          component: () => import('@/pages/logs/LogList.vue'),
          meta: { title: '操作日志', icon: 'schedule', requiresAuth: true }
        },
        {
          path: 'tasks',
          name: 'tasks',
          component: () => import('@/pages/tasks/TaskList.vue'),
          meta: { title: '任务列表', icon: 'schedule', requiresAuth: true }
        }
      ]
    }
  ]
})

// Auth guard
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/servers')
  } else {
    next()
  }
})

export default router
