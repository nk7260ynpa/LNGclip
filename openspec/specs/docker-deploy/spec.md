## ADDED Requirements

### Requirement: Docker Compose 編排

系統 SHALL 透過 Docker Compose 統一管理 frontend、backend、postgres、crawler 四個 container。

#### Scenario: 一鍵啟動

- **WHEN** 執行 `run.sh`
- **THEN** 依序啟動 postgres → backend + crawler → frontend 四個 container

#### Scenario: crawler 服務

- **WHEN** crawler container 啟動
- **THEN** crond 常駐運行，依排程每 3 天觸發爬蟲腳本

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

系統 SHALL 使用本地目錄掛載持久化 PostgreSQL 資料與影片縮圖。

#### Scenario: PostgreSQL 資料掛載

- **WHEN** Docker Compose 啟動 postgres 服務
- **THEN** 資料掛載至專案目錄的 `database/` 資料夾

#### Scenario: images 目錄掛載

- **WHEN** Docker Compose 啟動 backend 服務
- **THEN** `images/` 資料夾掛載至 backend container

#### Scenario: 重新啟動不遺失資料

- **WHEN** 執行 `docker compose down` 後再 `docker compose up`
- **THEN** PostgreSQL 資料透過 `database/` 目錄保留，不會遺失

### Requirement: 啟動腳本

系統 SHALL 提供 `run.sh` 腳本作為統一入口。

#### Scenario: 執行啟動腳本

- **WHEN** 執行 `./run.sh`
- **THEN** 腳本執行 docker compose build（若需要）並啟動所有服務

### Requirement: nginx API 代理 timeout

nginx SHALL 設定足夠的 proxy timeout，避免長時間 API 請求被中斷。

#### Scenario: 爬蟲 API 不 timeout

- **WHEN** 前端透過 nginx 呼叫 POST /api/crawl（耗時 3-4 分鐘）
- **THEN** nginx 等待最長 300 秒，不回傳 504
