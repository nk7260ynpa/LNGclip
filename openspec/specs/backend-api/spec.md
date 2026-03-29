## ADDED Requirements

### Requirement: 頻道 CRUD API

後端 SHALL 提供簡化的頻道 API。

#### Scenario: 取得所有頻道

- **WHEN** 前端發送 `GET /api/channels`
- **THEN** 回傳所有頻道列表（id、channel_id、channel_url）

#### Scenario: 新增頻道

- **WHEN** 前端發送 `POST /api/channels` 包含 `url` 欄位
- **THEN** 系統解析 URL 取得 channel_id，建立記錄並回傳 201

#### Scenario: 新增頻道 URL 無效

- **WHEN** 前端發送的 URL 無法解析出 channel_id
- **THEN** 回傳 400 錯誤，包含支援的 URL 格式說明

#### Scenario: 刪除頻道

- **WHEN** 前端發送 `DELETE /api/channels/{id}`
- **THEN** 系統刪除該頻道及其所有影片記錄，回傳 204
