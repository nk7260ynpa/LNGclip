## 1. 專案基礎建設

- [x] 1.1 建立專案目錄結構（src/、frontend/、docker/、tests/、logs/）
- [x] 1.2 建立 requirements.txt（FastAPI、SQLAlchemy、psycopg2-binary、APScheduler、feedparser、uvicorn）
- [x] 1.3 建立後端 Dockerfile（docker/Dockerfile，基於 Python 3.12）
- [x] 1.4 建立前端 Dockerfile（frontend/Dockerfile，多階段建置 Node + nginx）
- [x] 1.5 建立 docker-compose.yaml（frontend、backend、postgres 三個服務）
- [x] 1.6 建立 docker/build.sh 與 run.sh 啟動腳本

## 2. 資料庫與 ORM

- [x] 2.1 建立 src/config.py（資料庫連線、環境變數管理）
- [x] 2.2 建立 src/models/channel.py（channels 表 SQLAlchemy model）
- [x] 2.3 建立 src/models/video.py（videos 表 SQLAlchemy model，FK 關聯 channels）
- [x] 2.4 建立資料庫初始化邏輯（啟動時自動建表）

## 3. 後端 API

- [x] 3.1 建立 src/main.py（FastAPI 入口、CORS 設定、啟動事件）
- [x] 3.2 建立 src/schemas/（Pydantic request/response schemas）
- [x] 3.3 建立 src/api/channels.py（頻道 CRUD API：GET/POST/PUT/DELETE/PATCH toggle）
- [x] 3.4 建立 src/api/videos.py（影片查詢 API：GET /api/channels/{id}/videos）
- [x] 3.5 建立 src/api/sync.py（手動同步 API：POST /api/channels/{id}/sync、POST /api/sync）

## 4. RSS 同步服務

- [x] 4.1 建立 src/services/rss_sync.py（RSS Feed 抓取與解析邏輯）
- [x] 4.2 實作影片去重寫入（以 video_id 判斷是否為新影片）
- [x] 4.3 建立 src/services/scheduler.py（APScheduler 排程設定，每日定時執行）
- [x] 4.4 整合排程器至 FastAPI 啟動/關閉事件

## 5. 日誌系統

- [x] 5.1 建立 src/logging_config.py（logging 設定，輸出至 logs/ 目錄與 console）
- [x] 5.2 在 API routes 與 RSS 同步服務中加入日誌記錄

## 6. 前端 React 專案

- [x] 6.1 初始化 React 專案（frontend/，含 React Router 設定）
- [x] 6.2 建立 frontend/src/services/api.js（API 呼叫封裝）
- [x] 6.3 建立前台首頁（頻道卡片列表頁面）
- [x] 6.4 建立前台頻道詳細頁（影片列表頁面，點擊導向 YouTube）
- [x] 6.5 建立後台管理頁面（頻道表格、新增/編輯/刪除/啟用停用操作）
- [x] 6.6 設定 nginx 反向代理（前端靜態檔案 + API 轉發至 backend）

## 7. 測試

- [x] 7.1 建立後端單元測試（頻道 CRUD API 測試）
- [x] 7.2 建立 RSS 同步服務單元測試
- [x] 7.3 確認 Docker Compose 整合測試（三個服務正常啟動與連線）

## 8. 文件與收尾

- [x] 8.1 更新 README.md（專案說明、架構圖、啟動方式、環境變數說明）
- [x] 8.2 更新 .gitignore（加入 frontend/node_modules/、frontend/build/ 等）
- [x] 8.3 更新 CLAUDE.md（同步最新專案架構與開發慣例）
