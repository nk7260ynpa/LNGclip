## Why

目前前台使用 YouTube iframe 嵌入式播放器，載入速度慢且消耗資源。改為縮圖 + 超連結的方式更輕量，點擊後直接導向 YouTube 觀看。同時 PostgreSQL 資料目前存在 Docker named volume，不利於備份和版本管理，需改為掛載本地目錄。

## What Changes

- 前台影片從 iframe 嵌入改為縮圖顯示，點擊導向 YouTube 影片頁面
- 建立 `images/` 資料夾用於存放縮圖（含 .gitkeep）
- 建立 `database/` 資料夾用於 PostgreSQL 資料持久化（含 .gitkeep）
- docker-compose.yaml 將 postgres volume 從 named volume 改為掛載 `database/` 目錄
- docker-compose.yaml 掛載 `images/` 目錄至 backend container
- 確認資料搬移成功後刪除舊的 named volume

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `frontend-browse`: iframe 嵌入改為縮圖超連結
- `docker-deploy`: postgres 改用本地目錄掛載，新增 images 掛載

## Impact

- `frontend/src/pages/Home.js`：iframe 改為縮圖 + 連結
- `frontend/src/App.css`：調整卡片樣式
- `docker/docker-compose.yaml`：volume 改為 bind mount
- `images/`：新增目錄（含 .gitkeep）
- `database/`：新增目錄（含 .gitkeep）
- `.gitignore`：排除 database 內容、images 內容
