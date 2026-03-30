## ADDED Requirements

### Requirement: 靜態檔案服務

後端 SHALL 提供 `/api/images/` 靜態檔案服務，供前端讀取本地縮圖。

#### Scenario: 讀取縮圖

- **WHEN** 前端請求 `GET /api/images/{video_id}.jpg`
- **THEN** 回傳本地 images/ 目錄中對應的縮圖檔案
