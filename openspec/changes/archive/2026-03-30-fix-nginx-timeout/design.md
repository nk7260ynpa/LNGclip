## Context

1. 爬蟲 API 同步執行需 3-4 分鐘，nginx 預設 60 秒 timeout 導致 504。
2. 縮圖依賴 YouTube CDN，需改為本地儲存。images/ 目錄已建立並掛載至 backend container。

## Goals / Non-Goals

**Goals:**

- 修正 504 timeout 問題
- 抓取影片時下載縮圖到 images/ 目錄
- 後端提供靜態檔案服務供前端讀取本地縮圖

**Non-Goals:**

- 爬蟲改為背景非同步執行（之後再做）
- 縮圖壓縮或調整尺寸

## Decisions

### 1. proxy timeout 加到 300 秒

nginx `/api/` location 加上 proxy_read_timeout、proxy_connect_timeout、proxy_send_timeout 300s。

### 2. 縮圖下載邏輯

在 `fetch_channel_videos` 中，寫入 DB 時同步下載縮圖：

```python
import urllib.request

url = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"
path = f"/app/images/{video_id}.jpg"
urllib.request.urlretrieve(url, path)
```

使用 `urllib.request` 不需額外依賴。下載失敗不阻擋影片寫入。

### 3. FastAPI 靜態檔案服務

```python
from fastapi.staticfiles import StaticFiles
app.mount("/api/images", StaticFiles(directory="images"), name="images")
```

前端透過 `/api/images/{video_id}.jpg` 讀取，經 nginx 轉發至 backend。

### 4. thumbnail 欄位改存本地路徑

videos 表的 thumbnail 改存 `/api/images/{video_id}.jpg`，前端直接使用。

### 5. crawler container 也需掛載 images/

crawler 執行爬蟲時也會下載縮圖，需在 docker-compose.yaml 掛載 images/ 到 crawler container。

## Risks / Trade-offs

- **磁碟空間** → 每張縮圖約 10-20KB，1000 部影片約 15MB，可接受
- **下載失敗** → 記錄 WARNING，thumbnail 欄位保留 YouTube CDN URL 作為 fallback
