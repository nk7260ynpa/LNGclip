## Why

前台首頁目前只顯示頻道 ID 列表，沒有影片內容。需要在前台以 3x2 網格排列 YouTube 嵌入式影片播放器，將所有頻道的影片混合後依發佈時間由新到舊排列，讓使用者可直接在頁面上觀看最新精華影片。

## What Changes

- 前台首頁改為 3x2（每頁 6 部）嵌入式影片網格，使用 YouTube iframe embed
- 所有頻道影片混合，依 published_at 倒序排列（最新的排最前面）
- 後端新增全域影片查詢 API（跨頻道、支援分頁）
- 重新啟用 videos API router

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `frontend-browse`: 前台首頁改為嵌入式影片網格展示
- `backend-api`: 新增跨頻道影片查詢 API（分頁）

## Impact

- `frontend/src/pages/Home.js`：重寫為影片網格頁面
- `frontend/src/App.css`：新增影片網格樣式
- `frontend/src/services/api.js`：新增影片 API 呼叫
- `src/api/videos.py`：新增全域影片查詢端點
- `src/main.py`：重新註冊 videos router
