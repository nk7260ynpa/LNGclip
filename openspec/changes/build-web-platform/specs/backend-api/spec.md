## ADDED Requirements

### Requirement: 頻道 CRUD API

後端 SHALL 提供頻道的 RESTful CRUD API。

#### Scenario: 取得所有頻道

- **WHEN** 前端發送 `GET /api/channels`
- **THEN** 回傳所有頻道列表（可選 query parameter `active_only=true` 僅回傳啟用頻道）

#### Scenario: 取得單一頻道

- **WHEN** 前端發送 `GET /api/channels/{id}`
- **THEN** 回傳該頻道的完整資訊

#### Scenario: 新增頻道

- **WHEN** 前端發送 `POST /api/channels` 包含 channel_id、channel_name、streamer、description
- **THEN** 系統建立頻道記錄並回傳 201，同時觸發一次 RSS 同步

#### Scenario: 更新頻道

- **WHEN** 前端發送 `PUT /api/channels/{id}` 包含更新欄位
- **THEN** 系統更新頻道記錄並回傳更新後的資料

#### Scenario: 刪除頻道

- **WHEN** 前端發送 `DELETE /api/channels/{id}`
- **THEN** 系統刪除該頻道及其所有影片記錄，回傳 204

#### Scenario: 切換啟用狀態

- **WHEN** 前端發送 `PATCH /api/channels/{id}/toggle`
- **THEN** 系統切換 `is_active` 狀態並回傳更新後的頻道資料

### Requirement: 影片查詢 API

後端 SHALL 提供影片查詢 API。

#### Scenario: 取得頻道影片

- **WHEN** 前端發送 `GET /api/channels/{id}/videos`
- **THEN** 回傳該頻道的影片列表，依 published_at 倒序排列

#### Scenario: 頻道不存在

- **WHEN** 前端查詢不存在的頻道 ID
- **THEN** 回傳 404 錯誤

### Requirement: 手動觸發同步 API

後端 SHALL 提供手動觸發影片同步的 API。

#### Scenario: 同步單一頻道

- **WHEN** 前端發送 `POST /api/channels/{id}/sync`
- **THEN** 系統立即抓取該頻道的 RSS Feed 並更新影片資料，回傳同步結果（新增影片數）

#### Scenario: 同步所有頻道

- **WHEN** 前端發送 `POST /api/sync`
- **THEN** 系統抓取所有啟用頻道的 RSS Feed 並更新影片資料
