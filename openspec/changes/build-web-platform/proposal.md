## Why

LNGclip 目前僅有專案骨架，尚無實際功能。需要建立完整的 Web 平台，讓管理者可以透過後台管理 LNG 精華影片頻道，並在前台自動展示各頻道的最新影片，供個人瀏覽使用。

## What Changes

- 新增 React SPA 前端，包含前台（頻道與影片瀏覽）與後台（頻道 CRUD 管理）
- 新增 FastAPI 後端，提供 RESTful API
- 新增 PostgreSQL 資料庫，儲存頻道與影片資料
- 新增 APScheduler 定時排程，每日透過 YouTube RSS Feed 自動抓取各頻道最新影片
- 新增 Docker Compose 編排，統一管理 frontend、backend、postgres 三個 container

## Capabilities

### New Capabilities

- `frontend-browse`: 前台頻道與影片瀏覽頁面，展示所有啟用頻道及其最新影片
- `admin-manage`: 後台管理頁面，提供頻道的新增、編輯、刪除、啟用/停用功能
- `backend-api`: FastAPI 後端 RESTful API，處理頻道 CRUD 與影片查詢
- `video-sync`: 定時排程透過 YouTube RSS Feed 抓取各頻道最新影片並寫入資料庫
- `database`: PostgreSQL 資料庫 schema 設計（channels、videos 兩張表）
- `docker-deploy`: Docker Compose 編排，三個 container 的建置與啟動流程

### Modified Capabilities

- `channel-list`: 原有的頻道清單篩選排序規格，調整為透過 API 提供而非 CLI 輸出
- `channel-output`: 原有的 JSON 檔案輸出規格，調整為透過前端頁面展示

## Impact

- 新增 `frontend/` 目錄（React 專案）
- 新增 `src/` 目錄（FastAPI 後端）
- 新增 `docker/` 目錄（Dockerfile、docker-compose.yaml、build.sh）
- 新增 `run.sh` 啟動腳本
- 依賴：React、FastAPI、SQLAlchemy、APScheduler、psycopg2、feedparser
