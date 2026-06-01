# 云服务运维控制台

一个前后端分离的云服务运维管理工具前端项目，基于 Vue 3 + TypeScript + Element Plus 构建。

## 功能

- **服务器管理** — 查看服务器列表、启动/停止服务器，支持搜索和筛选
- **按量服务管理** — 管理按量计费云服务，一键启用/停用
- **定时任务** — 创建和管理定时开机/关机任务，支持 Cron 表达式
- **购买服务器** — 三步向导：选择实例规格 → 确认订单 → 完成购买
- **控制台首页** — 概览服务器状态、服务费用、定时任务等关键信息
- **暗色模式** — 支持亮色/暗色主题切换

## 技术栈

- **框架**: Vue 3 + Composition API + `<script setup>`
- **语言**: TypeScript (strict mode)
- **构建**: Vite 8
- **UI 组件库**: Element Plus 2.x
- **状态管理**: Pinia 3.x
- **路由**: Vue Router 4.x
- **HTTP 请求**: Axios + axios-mock-adapter (开发阶段 mock)
- **时间处理**: dayjs
- **包管理**: pnpm

## 快速开始

### 前置要求

- Node.js >= 18
- pnpm >= 8

### 安装与运行

```bash
# 安装依赖
pnpm install

# 启动开发服务器 (默认启用 Mock 数据)
pnpm dev

# 访问 http://localhost:5173
```

### 构建部署

```bash
# 构建生产版本
pnpm build

# 预览构建结果
pnpm preview
```

## 项目结构

```
src/
├── api/             # API 请求层 & Mock 数据
├── assets/          # 静态资源 & 样式
├── components/      # 可复用组件
│   ├── common/      # 通用组件 (StatusBadge, ConfirmDialog, EmptyState 等)
│   ├── server/      # 服务器相关组件
│   ├── service/     # 按量服务相关组件
│   ├── schedule/    # 定时任务相关组件
│   └── purchase/    # 购买相关组件
├── layouts/         # 布局组件 (侧边栏 + 顶栏)
├── pages/           # 页面组件
├── router/          # 路由配置
├── stores/          # Pinia 状态管理
├── types/           # TypeScript 类型定义
└── utils/           # 工具函数
```

## Mock 模式

项目默认使用 Mock 数据运行，无需后端服务。通过以下环境变量控制：

```
VITE_USE_MOCK=true   # 启用 Mock (默认)
VITE_USE_MOCK=false  # 连接真实后端
```

切换到真实后端时，只需修改 `.env` 文件中的 API 地址：

```
VITE_API_BASE_URL=https://your-api-server.com/api
VITE_USE_MOCK=false
```

## License

MIT
