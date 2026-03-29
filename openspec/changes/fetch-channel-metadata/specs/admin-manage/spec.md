## MODIFIED Requirements

### Requirement: 頻道列表管理

後台 SHALL 在 `/admin` 頁面展示頻道的完整資訊。

#### Scenario: 檢視管理列表

- **WHEN** 管理者進入 `/admin`
- **THEN** 頁面以表格形式顯示所有頻道，包含頻道名稱、channel_id、訂閱數、影片數

#### Scenario: 元資料未抓取

- **WHEN** 某頻道的 channel_name 為 NULL
- **THEN** 名稱欄顯示「未取得」，並提供「抓取」按鈕
