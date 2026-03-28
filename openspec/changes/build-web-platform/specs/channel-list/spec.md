## MODIFIED Requirements

### Requirement: 頻道清單篩選

系統 SHALL 透過後台管理的 `is_active` 狀態篩選頻道，前台僅顯示啟用的頻道。

#### Scenario: 前台僅顯示啟用頻道

- **WHEN** 前端請求頻道列表（`GET /api/channels?active_only=true`）
- **THEN** API 僅回傳 `is_active=true` 的頻道

#### Scenario: 後台顯示所有頻道

- **WHEN** 後台請求頻道列表（`GET /api/channels`）
- **THEN** API 回傳所有頻道，包含啟用與停用狀態

### Requirement: 頻道清單排序

系統 SHALL 依據頻道名稱對清單進行排序。

#### Scenario: 預設排序

- **WHEN** 未指定排序方式
- **THEN** 依頻道名稱字母順序排列

## REMOVED Requirements

### Requirement: 頻道去重

**Reason**: 頻道改為後台手動管理，channel_id 具有 UNIQUE 約束，不會產生重複。
**Migration**: 去重邏輯由資料庫 UNIQUE 約束取代。
