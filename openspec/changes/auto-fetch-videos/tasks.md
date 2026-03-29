## 1. DB Model 調整

- [ ] 1.1 src/models/video.py：video_id 從 VARCHAR(11) 改為 VARCHAR(32)

## 2. 影片抓取服務

- [ ] 2.1 新增 src/services/video_fetch.py（yt-dlp 抓取頻道最新 30 部影片並寫入 DB）

## 3. API 整合

- [ ] 3.1 src/api/channels.py：新增頻道後呼叫影片抓取服務

## 4. 測試與部署

- [ ] 4.1 更新 tests/test_channels_api.py（驗證新增頻道時影片抓取）
- [ ] 4.2 重建 Docker 服務、清除舊 DB 並驗證功能
