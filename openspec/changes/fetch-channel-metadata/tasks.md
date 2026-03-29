## 1. 後端 Model 與依賴

- [ ] 1.1 requirements.txt 新增 yt-dlp
- [ ] 1.2 src/models/channel.py 新增 channel_name、subscriber_count、video_count 欄位（NULLABLE）
- [ ] 1.3 src/schemas/channel.py ChannelResponse 新增對應欄位

## 2. 元資料抓取服務

- [ ] 2.1 新增 src/services/channel_metadata.py（使用 yt-dlp 抓取頻道名稱、訂閱數、影片數）

## 3. API 調整

- [ ] 3.1 src/api/channels.py：新增頻道後自動呼叫元資料抓取
- [ ] 3.2 src/api/channels.py：新增 POST /api/channels/{id}/fetch-metadata
- [ ] 3.3 src/api/channels.py：新增 POST /api/channels/backfill

## 4. 前端調整

- [ ] 4.1 Admin.js 列表顯示頻道名稱、訂閱數、影片數
- [ ] 4.2 Admin.js 未取得元資料的頻道顯示「抓取」按鈕
- [ ] 4.3 api.js 新增 fetchMetadata 與 backfillChannels 函式

## 5. 測試與部署

- [ ] 5.1 更新 tests/test_channels_api.py
- [ ] 5.2 重建 Docker image 並驗證功能
