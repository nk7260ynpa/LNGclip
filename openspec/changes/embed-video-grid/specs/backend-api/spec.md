## ADDED Requirements

### Requirement: 全域影片查詢 API

後端 SHALL 提供跨頻道的影片分頁查詢 API。

#### Scenario: 分頁查詢

- **WHEN** 前端發送 `GET /api/videos?page=1&per_page=6`
- **THEN** 回傳依 published_at 倒序排列的影片列表，包含總筆數與總頁數

#### Scenario: 預設分頁

- **WHEN** 前端發送 `GET /api/videos` 未帶分頁參數
- **THEN** 預設 page=1、per_page=6
