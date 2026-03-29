## 1. 後端 API

- [x] 1.1 src/api/videos.py：新增 GET /api/videos 全域影片分頁查詢（page、per_page、依 published_at DESC）
- [x] 1.2 src/main.py：重新註冊 videos router

## 2. 前端

- [x] 2.1 api.js：新增 getVideos(page, perPage) 函式
- [x] 2.2 Home.js：改為 3x2 嵌入式影片網格 + 分頁按鈕
- [x] 2.3 App.css：新增影片網格樣式（3 欄 grid、RWD）

## 3. 測試與部署

- [x] 3.1 重建前端 Docker image 並驗證頁面
