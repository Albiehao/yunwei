# 前端开发文档

## 项目概述

云服务运维控制台是一个运维管理工具的前端项目，用于管理云服务器实例的启停、按量服务、定时任务和实例购买。

## 架构设计

### 分层架构

```
页面层 (pages/)       ← 路由对应，负责页面布局和数据编排
   │
组件层 (components/)  ← 可复用的 UI 组件，纯展示+事件通知
   │
状态层 (stores/)      ← Pinia Store，管理业务数据和异步操作
   │
接口层 (api/)         ← Axios HTTP 请求 + Mock 适配
   │
类型层 (types/)       ← TypeScript 类型定义
```

### 数据流

1. 页面组件在 `onMounted` 中调用 Store Action
2. Store Action 调用 API 层函数
3. API 层通过 Axios 发送请求（Mock 模式下被 axios-mock-adapter 拦截）
4. 响应数据通过 Store 的状态（ref）响应式更新到视图

### 路由设计

| 路径 | 页面 | 说明 |
|------|------|------|
| `/dashboard` | Dashboard.vue | 控制台首页 |
| `/servers` | server/ServerList.vue | 服务器管理 |
| `/services` | service/ServiceList.vue | 按量服务 |
| `/schedules` | schedule/ScheduleList.vue | 定时任务 |
| `/purchase` | purchase/PurchaseServer.vue | 购买服务器 |

## 关键设计决策

### 1. Mock 层解耦

使用 `axios-mock-adapter` 在 Axios 层面拦截请求，通过 `VITE_USE_MOCK` 环境变量控制开关。切换到真实后端时只需关闭 Mock 并修改 API 地址。

### 2. 组件三态覆盖

所有数据展示组件必须覆盖三种状态：
- **Loading** — 使用 SkeletonLoader 骨架屏组件
- **Empty** — 使用 EmptyState 空状态组件（含引导操作）
- **Error** — 使用 el-alert + 重试按钮

### 3. 异步状态模拟

服务器启停操作在 Mock 层模拟异步状态转换：
- 启动：`stopped (点击) → starting (2-3s) → running`
- 停止：`running (点击) → stopping (2-3s) → stopped`

### 4. 暗色模式

使用 Element Plus 的 `dark.css` + CSS 变量覆盖，通过 `html.dark` 类控制，偏好持久化到 `localStorage`。

## 扩展指南

### 添加新的 API 端点

1. 在 `src/types/` 中添加类型定义
2. 在 `src/api/` 中添加 API 函数
3. 在 `src/api/mock.ts` 中添加 Mock 数据和拦截器
4. 在 `src/stores/` 中添加 Store Action

### 添加新的页面

1. 在 `src/pages/` 下创建页面组件
2. 在 `src/router/index.ts` 中添加路由
3. 在 `src/layouts/AppSidebar.vue` 的 `menuItems` 中添加菜单项

### 添加新的组件

1. 在 `src/components/` 下按模块创建目录
2. 创建 `index.ts` 统一导出

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `VITE_API_BASE_URL` | API 基础路径 | `/api` |
| `VITE_USE_MOCK` | 是否启用 Mock | `true` |

## 常用命令

```bash
pnpm dev          # 启动开发服务器
pnpm build        # 构建生产版本
pnpm preview      # 预览构建结果
pnpm lint         # 代码检查
```
