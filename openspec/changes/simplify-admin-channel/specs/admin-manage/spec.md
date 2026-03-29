## MODIFIED Requirements

### Requirement: 新增頻道

後台 SHALL 提供新增頻道的表單，管理者只需輸入 YouTube 頻道網址即可完成新增。

#### Scenario: 填寫並送出新增表單

- **WHEN** 管理者貼上 YouTube 頻道網址並送出
- **THEN** 系統解析 channel_id，建立頻道記錄（不觸發 RSS 同步）

#### Scenario: channel_id 重複

- **WHEN** 解析出的 channel_id 已存在於資料庫
- **THEN** 顯示錯誤提示「此頻道已存在」

#### Scenario: 無效的 URL

- **WHEN** 管理者輸入的網址無法解析出 channel_id
- **THEN** 顯示錯誤提示，說明支援的 URL 格式

### Requirement: 頻道列表管理

後台 SHALL 在 `/admin` 頁面展示所有頻道的管理列表，提供刪除操作。

#### Scenario: 檢視管理列表

- **WHEN** 管理者進入 `/admin`
- **THEN** 頁面以表格形式顯示所有頻道，包含 channel_id 與 channel_url

### Requirement: 刪除頻道

後台 SHALL 提供刪除頻道的功能。

#### Scenario: 確認刪除

- **WHEN** 管理者點擊「刪除」並確認
- **THEN** 系統刪除該頻道記錄及其關聯的所有影片

## REMOVED Requirements

### Requirement: 編輯頻道

**Reason**: channels 表簡化為 3 個欄位，無需編輯功能。
**Migration**: 如需修改，刪除後重新新增。

### Requirement: 啟用/停用頻道

**Reason**: 移除 is_active 欄位，不再有啟用/停用狀態。
**Migration**: 不需要的頻道直接刪除。
