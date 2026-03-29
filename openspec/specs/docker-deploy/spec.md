## ADDED Requirements

### Requirement: Docker Compose 編排

系統 SHALL 透過 Docker Compose 統一管理 frontend、backend、postgres 三個 container。

#### Scenario: 一鍵啟動

- **WHEN** 執行 `run.sh`
- **THEN** 依序啟動 postgres → backend → frontend 三個 container，並確保健康檢查通過後才啟動依賴服務

#### Scenario: 服務埠號

- **WHEN** 所有 container 啟動完成
- **THEN** frontend 對外開放 port 3001，backend 對外開放 port 8001，postgres 對外開放 port 5433

### Requirement: 後端 Docker 映像

系統 SHALL 提供後端的 Dockerfile，基於 Python 3.12 建置。

#### Scenario: 建置後端映像

- **WHEN** 執行 `docker/build.sh`
- **THEN** 建置包含 FastAPI 應用與所有依賴的 Docker 映像

### Requirement: 前端 Docker 映像

系統 SHALL 提供前端的 Dockerfile，使用多階段建置（Node build + nginx serve）。

#### Scenario: 建置前端映像

- **WHEN** Docker Compose 建置前端服務
- **THEN** 先以 Node 環境執行 `npm run build`，再以 nginx 提供靜態檔案

### Requirement: 資料持久化

系統 SHALL 使用 Docker volume 持久化 PostgreSQL 資料。

#### Scenario: 重新啟動不遺失資料

- **WHEN** 執行 `docker compose down` 後再 `docker compose up`
- **THEN** PostgreSQL 資料透過 named volume 保留，不會遺失

### Requirement: 啟動腳本

系統 SHALL 提供 `run.sh` 腳本作為統一入口。

#### Scenario: 執行啟動腳本

- **WHEN** 執行 `./run.sh`
- **THEN** 腳本執行 docker compose build（若需要）並啟動所有服務
