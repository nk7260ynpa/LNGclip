## Why

目前 channels 表只存 id、channel_id、channel_url，前台無法顯示頻道名稱、訂閱數、影片數等資訊。需要在新增頻道時自動抓取這些資料，並補足現有頻道缺失的資料。

## What Changes

- channels 表新增 `channel_name`、`subscriber_count`、`video_count` 三個欄位
- 新增頻道時，後端使用 yt-dlp 自動抓取頻道元資料並寫入 DB
- 提供 API 端點補足已有頻道缺失的元資料
- 後台管理列表顯示頻道名稱、訂閱數、影片數

## Capabilities

### New Capabilities

- `channel-metadata`: 使用 yt-dlp 從 YouTube 抓取頻道元資料（名稱、訂閱數、影片數）

### Modified Capabilities

- `database`: channels 表新增 channel_name、subscriber_count、video_count 欄位
- `backend-api`: 新增頻道時自動抓取元資料，新增 backfill API
- `admin-manage`: 後台列表顯示頻道名稱、訂閱數、影片數

## Impact

- `requirements.txt`：新增 yt-dlp 依賴
- `src/models/channel.py`：新增 3 個欄位
- `src/schemas/channel.py`：ChannelResponse 新增欄位
- `src/services/channel_metadata.py`：新增元資料抓取服務
- `src/api/channels.py`：新增時觸發元資料抓取、新增 backfill API
- `frontend/src/pages/Admin.js`：列表顯示新欄位
- `docker/Dockerfile`：需安裝 yt-dlp（含 ffmpeg 可選）
