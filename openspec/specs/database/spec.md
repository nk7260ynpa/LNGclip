## ADDED Requirements

### Requirement: channels 資料表

系統 SHALL 維護簡化的 channels 資料表，僅儲存頻道識別資訊。

#### Scenario: 資料表欄位定義

- **WHEN** 資料庫初始化
- **THEN** channels 表包含以下欄位：
  - `id` SERIAL PRIMARY KEY
  - `channel_id` VARCHAR(24) UNIQUE NOT NULL（YouTube 頻道識別碼）
  - `channel_url` VARCHAR NOT NULL（使用者輸入的原始網址）

### Requirement: 資料庫自動遷移

系統 SHALL 在啟動時自動建立或更新資料表結構。

#### Scenario: 首次啟動

- **WHEN** 後端服務首次啟動且資料表不存在
- **THEN** 系統透過 SQLAlchemy 自動建立所有資料表
