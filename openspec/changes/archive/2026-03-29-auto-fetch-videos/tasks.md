## 1. DB Model 調整

- [x] 1.1 src/models/video.py：video_id 從 VARCHAR(11) 改為 VARCHAR(32)
- [x] 1.2 src/models/video.py：channel_id FK 改為 VARCHAR 參照 channels.channel_id

## 2. 影片抓取服務

- [x] 2.1 新增 src/services/video_fetch.py（yt-dlp 抓取頻道最新 30 部影片並寫入 DB）
- [x] 2.2 video_fetch.py：寫入影片時 channel_id 改用 channels.channel_id 值

## 3. API 整合

- [x] 3.1 src/api/channels.py：新增頻道後呼叫影片抓取服務

## 4. 測試與部署

- [x] 4.1 更新 tests/test_channels_api.py（驗證新增頻道時影片抓取）
- [x] 4.2 重建 Docker 服務、清除舊 DB 並驗證功能
