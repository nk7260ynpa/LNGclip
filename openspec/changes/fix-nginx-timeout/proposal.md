## Why

1. 前端點擊「檢查新影片」時，爬蟲需要 3-4 分鐘完成，但 nginx 的 proxy_read_timeout 預設 60 秒，導致 HTTP 504 Gateway Timeout。
2. 影片縮圖目前依賴 YouTube CDN（`i.ytimg.com`），載入速度受外部網路影響。需改為本地儲存縮圖，由 backend 提供靜態檔案服務。

## What Changes

- nginx.conf 的 `/api/` location 加上 `proxy_read_timeout 300s`，允許最長 5 分鐘的等待時間
- 抓取影片時同步下載縮圖到 `images/` 目錄，以 `{video_id}.jpg` 命名
- 後端提供 `/images/` 靜態檔案服務
- 前端縮圖 URL 改為讀取本地 `/api/images/{video_id}.jpg`
- videos 表的 thumbnail 欄位改存本地路徑

## Capabilities

### New Capabilities

- `thumbnail-download`: 抓取影片時下載縮圖到本地 images/ 目錄

### Modified Capabilities

- `docker-deploy`: nginx 反向代理 timeout 設定
- `backend-api`: 提供 images 靜態檔案服務
- `frontend-browse`: 縮圖改讀本地路徑
- `video-fetch`: 抓取影片時同步下載縮圖

## Impact

- `frontend/nginx.conf`：新增 proxy timeout 設定
- `src/services/video_fetch.py`：抓取時下載縮圖到 images/
- `src/main.py`：掛載 images/ 靜態檔案服務
- `frontend/src/pages/Home.js`：縮圖 URL 改為本地路徑
- `images/`：儲存下載的縮圖（已掛載至 backend container）
