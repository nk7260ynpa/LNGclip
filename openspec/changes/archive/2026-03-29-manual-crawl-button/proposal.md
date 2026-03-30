## Why

目前爬蟲只能透過 cron 每 3 天自動執行或進入 container 手動執行，使用者無法從網頁上觸發。需要在前端新增一個按鈕，讓使用者可以隨時強制執行爬蟲檢查所有頻道的新影片。

## What Changes

- 後端新增 API 端點，觸發所有頻道的影片爬蟲
- 前端首頁新增「檢查新影片」按鈕，呼叫該 API 並顯示結果

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `backend-api`: 新增手動觸發爬蟲的 API 端點
- `frontend-browse`: 首頁新增爬蟲觸發按鈕

## Impact

- `src/api/videos.py`：新增 POST /api/crawl 端點
- `frontend/src/pages/Home.js`：新增按鈕與呼叫邏輯
- `frontend/src/services/api.js`：新增 crawl API 函式
