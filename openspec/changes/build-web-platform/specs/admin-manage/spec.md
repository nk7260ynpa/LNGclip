## ADDED Requirements

### Requirement: 頻道列表管理

後台 SHALL 在 `/admin` 頁面展示所有頻道（含停用）的管理列表，提供新增、編輯、刪除操作入口。

#### Scenario: 檢視管理列表

- **WHEN** 管理者進入 `/admin`
- **THEN** 頁面以表格形式顯示所有頻道，包含頻道名稱、實況主、啟用狀態、影片數量、最後同步時間

### Requirement: 新增頻道

後台 SHALL 提供新增頻道的表單，管理者填入頻道資訊後送出即完成新增。

#### Scenario: 填寫並送出新增表單

- **WHEN** 管理者點擊「新增頻道」並填入 channel_id、頻道名稱、實況主名稱、說明
- **THEN** 系統建立頻道記錄，預設 `is_active=true`，並立即觸發一次 RSS 影片抓取

#### Scenario: channel_id 重複

- **WHEN** 管理者輸入的 channel_id 已存在於資料庫
- **THEN** 顯示錯誤提示「此頻道已存在」

### Requirement: 編輯頻道

後台 SHALL 提供編輯頻道資訊的功能。

#### Scenario: 修改頻道資訊

- **WHEN** 管理者點擊某頻道的「編輯」按鈕並修改欄位後送出
- **THEN** 系統更新該頻道記錄並反映在管理列表上

### Requirement: 刪除頻道

後台 SHALL 提供刪除頻道的功能，刪除時一併移除該頻道的所有影片資料。

#### Scenario: 確認刪除

- **WHEN** 管理者點擊「刪除」並確認
- **THEN** 系統刪除該頻道及其關聯的所有影片記錄

### Requirement: 啟用/停用頻道

後台 SHALL 提供切換頻道啟用狀態的功能，停用的頻道不會出現在前台，也不會被排程抓取。

#### Scenario: 停用頻道

- **WHEN** 管理者將頻道設為停用
- **THEN** 該頻道的 `is_active` 設為 `false`，前台不再顯示，排程跳過該頻道

#### Scenario: 重新啟用頻道

- **WHEN** 管理者將停用頻道重新啟用
- **THEN** 該頻道的 `is_active` 設為 `true`，並立即觸發一次 RSS 影片抓取
