## 1. 修正 nginx timeout

- [x] 1.1 frontend/nginx.conf：/api/ location 新增 proxy timeout 300s

## 2. 縮圖本地化

- [x] 2.1 src/services/video_fetch.py：抓取影片時下載縮圖到 images/，thumbnail 存本地路徑
- [x] 2.2 src/main.py：掛載 /api/images 靜態檔案服務
- [x] 2.3 docker-compose.yaml：crawler container 新增 images/ 掛載
- [x] 2.4 frontend/src/pages/Home.js：縮圖 URL 使用 thumbnail 欄位（本地路徑）—— 已使用 v.thumbnail，無需修改

## 3. 現有資料補足

- [x] 3.1 撰寫腳本下載現有影片的縮圖並更新 DB thumbnail 欄位

## 4. 測試與部署

- [x] 4.1 重建所有 Docker 服務並驗證功能（nginx timeout + 本地縮圖）
