## 1. 爬蟲腳本

- [x] 1.1 新增 src/crawler.py（遍歷所有頻道、呼叫 fetch_channel_videos、記錄結果）

## 2. Docker 設定

- [x] 2.1 新增 docker/Dockerfile.crawler（Python 3.12 + cron + crontab 設定）
- [x] 2.2 docker-compose.yaml 新增 crawler 服務（depends_on postgres、掛載 logs）

## 3. 測試與部署

- [x] 3.1 手動執行 crawler 腳本驗證功能
- [x] 3.2 重啟 Docker Compose 驗證 crawler container 正常運行
