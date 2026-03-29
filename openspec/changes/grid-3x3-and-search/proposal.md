## Why

目前前台每頁只顯示 6 部影片（3x2），內容偏少。同時缺少搜尋功能，無法快速找到特定影片。需要增加每頁顯示數量並新增標題搜尋。

## What Changes

- 前台網格從 3x2（每頁 6 部）改為 3x3（每頁 9 部）
- 確保影片依 published_at 倒序排列（最新上傳排最前）
- 新增搜尋列，支援依影片標題模糊搜尋
- 後端影片 API 新增 search query parameter

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `frontend-browse`: 網格改為 3x3，新增搜尋列
- `backend-api`: 影片 API 新增 search 參數

## Impact

- `frontend/src/pages/Home.js`：per_page 改為 9，新增搜尋輸入框
- `src/api/videos.py`：新增 search query parameter
