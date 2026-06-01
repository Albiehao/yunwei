import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('@/pages/Dashboard.vue'),
        meta: { title: '控制台', icon: 'Monitor' }
      },
      {
        path: 'servers',
        name: 'servers',
        component: () => import('@/pages/server/ServerList.vue'),
        meta: { title: '服务器管理', icon: 'Server' }
      },
      {
        path: 'services',
        name: 'services',
        component: () => import('@/pages/service/ServiceList.vue'),
        meta: { title: '按量服务', icon: 'Coin' }
      },
      {
        path: 'schedules',
        name: 'schedules',
        component: () => import('@/pages/schedule/ScheduleList.vue'),
        meta: { title: '定时任务', icon: 'Clock' }
      },
      {
        path: 'purchase',
        name: 'purchase',
        component: () => import('@/pages/purchase/PurchaseServer.vue'),
        meta: { title: '购买服务器', icon: 'ShoppingCart' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
