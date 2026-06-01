# 构建阶段：前端
FROM node:20-alpine AS frontend
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install
COPY . .
RUN corepack enable && pnpm build

# 运行阶段：后端
FROM python:3.12-slim
WORKDIR /app

# 系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# 后端依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 后端代码
COPY backend/ .

# 前端构建产物
COPY --from=frontend /app/dist /app/dist

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
