#!/bin/bash
#
# 啟動 LNGclip 所有服務（frontend、backend、postgres）

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly COMPOSE_FILE="${SCRIPT_DIR}/docker/docker-compose.yaml"

# 確保 logs 目錄存在
mkdir -p "${SCRIPT_DIR}/logs"

# 建置並啟動所有服務
docker compose -f "${COMPOSE_FILE}" up --build -d

echo "LNGclip 服務已啟動："
echo "  前台：http://localhost:3001"
echo "  後端 API：http://localhost:8001"
echo "  API 文件：http://localhost:8001/docs"
