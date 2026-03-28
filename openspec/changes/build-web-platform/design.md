## Context

LNGclip 目前僅有專案骨架（README、LICENSE、.gitignore、OpenSpec 設定）。需要從零建立完整的 Web 平台，包含前端、後端、資料庫與定時排程。此為個人使用的工具，不需要考慮高併發或複雜的權限系統。

## Goals / Non-Goals

**Goals:**

- 建立可運作的前後端分離 Web 平台
- 後台可管理 YouTube 精華頻道（CRUD）
- 前台可瀏覽頻道及其最新影片
- 每日自動透過 RSS Feed 同步最新影片
- 透過 Docker Compose 一鍵啟動所有服務

**Non-Goals:**

- 使用者認證/授權（個人使用，不需登入）
- YouTube Data API v3 整合（未來再考慮）
- 影片播放功能（點擊後導向 YouTube）
- SEO 優化或 SSR
- 多語系支援

## Decisions

### 1. 前端架構：React SPA + React Router

使用 React 搭配 React Router 實現前台與後台的路由切換。

- 前台路由：`/`（頻道列表）、`/channel/:id`（頻道影片）
- 後台路由：`/admin`（頻道管理）

**替代方案**：Vue.js — 學習曲線更低，但使用者選擇 React。

### 2. 後端框架：FastAPI

選擇 FastAPI 作為後端框架，搭配 SQLAlchemy ORM 操作資料庫。

- 非同步支援，適合 I/O 密集的 RSS 抓取
- 自動產生 OpenAPI 文件，方便前端對接
- Python 生態系統一致

**替代方案**：Flask — 更成熟但缺少原生非同步支援與自動 API 文件。

### 3. 資料庫：PostgreSQL + SQLAlchemy

使用 PostgreSQL 作為主要資料庫，透過 SQLAlchemy ORM 存取。

- channels 表：儲存頻道基本資訊與管理狀態
- videos 表：儲存從 RSS 抓取的影片資料，以 channel_id 做 FK 關聯

**替代方案**：SQLite — 更輕量但不適合 Docker 多 container 環境，且使用者選擇 PostgreSQL。

### 4. 影片同步：APScheduler + feedparser

使用 APScheduler 內建於 FastAPI 進程，每日固定時間執行 RSS 抓取任務。

- 使用 feedparser 解析 YouTube RSS Feed（`https://www.youtube.com/feeds/videos.xml?channel_id=XXX`）
- 每次抓取最新 15 部影片（RSS Feed 上限）
- 以 video_id 做去重，僅寫入新影片
- 新增頻道時立即觸發一次抓取

**替代方案**：Celery + Beat — 功能更強大但對此規模過度設計。

### 5. 專案目錄結構

```
LNGclip/
├── frontend/                 # React 前端
│   ├── src/
│   │   ├── components/       # 共用元件
│   │   ├── pages/            # 頁面元件
│   │   ├── services/         # API 呼叫
│   │   └── App.jsx
│   ├── package.json
│   └── Dockerfile
├── src/                      # FastAPI 後端
│   ├── api/                  # API routes
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # 業務邏輯（RSS 同步等）
│   ├── config.py             # 設定管理
│   └── main.py               # FastAPI 入口
├── tests/                    # 後端單元測試
├── docker/
│   ├── build.sh
│   ├── Dockerfile            # 後端 Dockerfile
│   └── docker-compose.yaml   # 三個 container 編排
├── logs/
├── run.sh                    # 一鍵啟動腳本
└── requirements.txt
```

### 6. Docker Compose 編排

三個 container：

| Container | Image | Port | 說明 |
|---|---|---|---|
| frontend | Node + nginx | 3000 | React build 後由 nginx 提供靜態檔案 |
| backend | Python 3.12 | 8000 | FastAPI 應用 |
| postgres | postgres:16 | 5432 | 資料庫，data volume 持久化 |

後端透過環境變數 `DATABASE_URL` 連接 PostgreSQL。

## Risks / Trade-offs

- **RSS Feed 限制** → 每個頻道僅提供最新 15 部影片，無法取得歷史完整影片列表。對於精華頻道瀏覽已足夠。
- **APScheduler 單進程** → 排程器與 API 共用同一進程，若 API 重啟則排程也重啟。以此規模可接受，未來可分離為獨立 worker。
- **無認證保護** → 後台管理頁面無需登入，任何能連線的人都可操作。僅限個人或內網使用。
- **前端 build 大小** → React SPA 包含前台與後台，bundle size 較大。個人使用不影響體驗。
