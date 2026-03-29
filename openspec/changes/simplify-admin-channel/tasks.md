## 1. 後端 Model 與 Schema 調整

- [x] 1.1 簡化 src/models/channel.py（僅保留 id、channel_id、channel_url）
- [x] 1.2 簡化 src/schemas/channel.py（ChannelCreate 改為只有 url 欄位，ChannelResponse 對應 3 欄位）
- [x] 1.3 新增 src/services/url_parser.py（從 YouTube URL 解析 channel_id）

## 2. 後端 API 調整

- [ ] 2.1 簡化 src/api/channels.py（保留 GET list、POST create、DELETE，移除 PUT、PATCH、get single）
- [ ] 2.2 移除 src/api/videos.py 與 src/api/sync.py 的 router 註冊
- [ ] 2.3 修改 src/main.py（移除排程器啟動、移除 sync/videos router）

## 3. 前端調整

- [ ] 3.1 簡化 Admin.js（新增表單改為只輸入 URL，移除編輯/同步/啟停用按鈕）
- [ ] 3.2 簡化 Home.js（暫時顯示 channel_id 列表）
- [ ] 3.3 簡化 ChannelDetail.js（暫時顯示 channel_id 基本資訊）
- [ ] 3.4 更新 api.js（移除不再使用的 API 呼叫函式）

## 4. 測試與收尾

- [ ] 4.1 更新 tests/test_channels_api.py（配合新 schema 調整測試案例）
- [ ] 4.2 更新 tests/test_rss_sync.py（暫時跳過或移除）
- [ ] 4.3 重新建置並啟動 Docker 服務驗證功能
