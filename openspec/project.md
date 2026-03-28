# LNGclip

## 說明

LNGclip 是一個用於蒐集並列出 LNG（遊戲實況主）精華影片頻道資訊的工具。彙整頻道基本資料（名稱、訂閱數、影片數、最新更新時間等），提供結構化的頻道清單輸出。

## 技術棧

- Python 3.12+
- Docker（執行環境）
- logging（日誌記錄）

## 程式碼慣例

- 遵循 Google Python Style Guide
- Docstring 與註解使用繁體中文
- 使用 logging 套件記錄日誌，日誌存放於 `logs/`
- 單元測試在 Docker container 中執行
- Git commit message 使用繁體中文，遵循 Conventional Commits

## 架構

- 入口腳本：`run.sh`（啟動 Docker container 並執行主程式）
- Docker 相關檔案：`docker/`（build.sh、Dockerfile、docker-compose.yaml）
- 主程式：`src/` 目錄
- 測試：`tests/` 目錄
- 日誌：`logs/` 目錄
- 輸出結果：JSON 格式

## 領域知識

- LNG 為台灣知名遊戲實況主，活躍於 YouTube 與 Twitch 平台
- 精華影片頻道為粉絲或官方經營的剪輯頻道，彙整直播精彩片段
- 常見的精華頻道名稱包含「LNG」與「精華」等關鍵字
