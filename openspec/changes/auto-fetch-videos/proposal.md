## Why

目前 videos 表是空的，新增頻道時不會抓取任何影片資料。需要在新增頻道時自動抓取最新 30 部影片並存入 DB，讓前台有內容可展示。同時 video_id 欄位長度限制 VARCHAR(11) 過於嚴格，需放寬以避免未來 YouTube 調整 ID 格式時出錯。

## What Changes

- `video_id` 欄位從 VARCHAR(11) 放寬為 VARCHAR(32)
- videos 表的 `channel_id` FK 改為 VARCHAR 參照 `channels.channel_id`，使兩表的 channel_id 語意一致
- 新增頻道時，使用 yt-dlp 自動抓取該頻道最新 30 部影片的資訊並寫入 videos 表
- 新增影片抓取服務，從 yt-dlp 取得影片 ID、標題、縮圖、發佈時間

## Capabilities

### New Capabilities

- `video-fetch`: 使用 yt-dlp 抓取頻道最新影片列表並寫入 DB

### Modified Capabilities

- `database`: video_id 欄位長度放寬為 VARCHAR(32)
- `backend-api`: 新增頻道時自動觸發影片抓取

## Impact

- `src/models/video.py`：video_id 長度調整
- `src/services/video_fetch.py`：新增影片抓取服務
- `src/api/channels.py`：新增頻道後觸發影片抓取
