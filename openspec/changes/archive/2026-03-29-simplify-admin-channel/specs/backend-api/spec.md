## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: 影片查詢 API

**Reason**: 前台功能暫時停用，之後再規劃。
**Migration**: 保留 videos 表結構，API 之後恢復。

### Requirement: 手動觸發同步 API

**Reason**: RSS 同步功能暫時停用。
**Migration**: 之後恢復排程時一併恢復。

### Requirement: 切換啟用狀態

**Reason**: 移除 is_active 欄位。
**Migration**: 不需要的頻道直接刪除。

### Requirement: 更新頻道

**Reason**: channels 表只有 3 個欄位，無需更新 API。
**Migration**: 刪除後重新新增。

### Requirement: 取得單一頻道

**Reason**: 簡化階段不需要單一頻道詳情。
**Migration**: 之後有頻道詳情需求時恢復。
