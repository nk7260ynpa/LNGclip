## 1. 前端：縮圖取代 iframe

- [x] 1.1 Home.js：iframe 改為縮圖 img + YouTube 超連結（開新分頁）
- [x] 1.2 App.css：調整 embed-card 樣式（縮圖 + hover 效果）

## 2. 本地目錄建立

- [x] 2.1 建立 images/ 資料夾（含 .gitkeep）
- [x] 2.2 建立 database/ 資料夾（含 .gitkeep）
- [x] 2.3 更新 .gitignore（排除 database/* 和 images/* 內容，保留 .gitkeep）

## 3. Docker 掛載調整

- [x] 3.1 停止服務，將 named volume 資料複製到 database/ 目錄
- [x] 3.2 docker-compose.yaml：postgres 改為 bind mount database/，新增 images/ 掛載至 backend
- [x] 3.3 移除 docker-compose.yaml 的 named volume 定義
- [x] 3.4 啟動服務，驗證資料完整（channels 與 videos 筆數正確）
- [x] 3.5 刪除舊的 docker_pgdata named volume
