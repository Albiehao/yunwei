# 构建阶段：前端
FROM node:22-alpine AS frontend
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# 运行阶段：后端
FROM python:3.12-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY --from=frontend /app/dist /app/dist

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
