## 1. 後端

- [x] 1.1 src/api/videos.py：新增 POST /api/crawl（遍歷所有頻道、呼叫 fetch_channel_videos、回傳結果）

## 2. 前端

- [x] 2.1 api.js：新增 triggerCrawl 函式（較長 timeout）
- [x] 2.2 Home.js：標題旁新增「檢查新影片」按鈕（loading 狀態、完成後重載影片）

## 3. 測試與部署

- [x] 3.1 重建 Docker 服務並驗證功能
