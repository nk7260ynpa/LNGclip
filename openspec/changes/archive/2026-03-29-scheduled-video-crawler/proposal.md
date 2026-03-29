## Why

目前影片只在新增頻道時抓取一次（最新 30 部），之後不會自動更新。需要獨立的爬蟲 container 定期檢查各頻道是否有新影片，確保前台展示的內容持續更新。

## What Changes

- 新增 crawler Docker container，獨立執行爬蟲任務
- 建立爬蟲腳本，遍歷所有頻道，使用 yt-dlp 抓取最新影片，以 video_id 去重後寫入 videos 表
- 使用 cron 排程每 3 天自動執行一次
- docker-compose.yaml 新增 crawler 服務

## Capabilities

### New Capabilities

- `video-crawler`: 獨立爬蟲 container，定期檢查並抓取新影片

### Modified Capabilities

- `docker-deploy`: docker-compose.yaml 新增 crawler 服務

## Impact

- `src/crawler.py`：新增爬蟲入口腳本
- `docker/Dockerfile.crawler`：爬蟲 container 的 Dockerfile
- `docker/docker-compose.yaml`：新增 crawler 服務
- 複用現有 `src/services/video_fetch.py` 的 `fetch_channel_videos`
