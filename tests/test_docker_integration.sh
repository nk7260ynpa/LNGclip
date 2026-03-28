#!/bin/bash
#
# Docker Compose 整合測試
# 驗證三個服務能正常啟動與連線

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly COMPOSE_FILE="${SCRIPT_DIR}/../docker/docker-compose.yaml"

echo "=== 啟動服務 ==="
docker compose -f "${COMPOSE_FILE}" up --build -d

echo "=== 等待服務就緒 ==="
sleep 10

echo "=== 測試後端健康檢查 ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health)
if [ "${HTTP_CODE}" -eq 200 ]; then
  echo "後端 API：OK (${HTTP_CODE})"
else
  echo "後端 API：FAIL (${HTTP_CODE})"
  docker compose -f "${COMPOSE_FILE}" logs backend
  docker compose -f "${COMPOSE_FILE}" down
  exit 1
fi

echo "=== 測試前端頁面 ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "${HTTP_CODE}" -eq 200 ]; then
  echo "前端頁面：OK (${HTTP_CODE})"
else
  echo "前端頁面：FAIL (${HTTP_CODE})"
  docker compose -f "${COMPOSE_FILE}" logs frontend
  docker compose -f "${COMPOSE_FILE}" down
  exit 1
fi

echo "=== 測試 API 透過 nginx 轉發 ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health)
if [ "${HTTP_CODE}" -eq 200 ]; then
  echo "nginx 轉發：OK (${HTTP_CODE})"
else
  echo "nginx 轉發：FAIL (${HTTP_CODE})"
fi

echo "=== 清理 ==="
docker compose -f "${COMPOSE_FILE}" down

echo "=== 整合測試完成 ==="
