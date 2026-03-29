## Why

目前後台新增頻道需要手動填入 5 個欄位（channel_id、channel_name、streamer、description、thumbnail），操作繁瑣。簡化為只需貼上 YouTube 頻道網址，後端自動解析 channel_id 並存入資料庫，大幅降低管理門檻。

## What Changes

- **BREAKING** 簡化 channels 資料表，僅保留 `id`、`channel_id`、`channel_url` 三個欄位，移除 `channel_name`、`streamer`、`description`、`thumbnail`、`is_active`、`updated_at`
- 後台新增頻道改為只輸入 YouTube 頻道網址
- 後端新增 URL 解析邏輯，從網址提取 channel_id
- 移除新增頻道時自動觸發 RSS 同步的行為
- 暫時停用前台頁面、RSS 排程同步功能（之後再規劃）

## Capabilities

### New Capabilities

- `url-parse`: 從 YouTube 頻道網址解析出 channel_id，支援多種 URL 格式

### Modified Capabilities

- `admin-manage`: 後台管理頁面簡化為只輸入網址，移除其他欄位的表單
- `backend-api`: 頻道 API 配合新的 DB schema 調整，新增時只需提供 URL
- `database`: channels 資料表精簡為 3 個欄位

## Impact

- `src/models/channel.py`：重新定義 Channel model
- `src/schemas/channel.py`：簡化 Pydantic schemas
- `src/api/channels.py`：調整 CRUD API 邏輯，移除同步觸發
- `frontend/src/pages/Admin.js`：簡化新增表單
- `frontend/src/pages/Home.js`：暫時顯示 channel_id（無頻道名稱）
- `frontend/src/pages/ChannelDetail.js`：同上調整
- `src/services/rss_sync.py`、`src/services/scheduler.py`：暫時停用
- `src/main.py`：移除排程器啟動
