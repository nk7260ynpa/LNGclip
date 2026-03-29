## MODIFIED Requirements

### Requirement: channels 資料表

系統 SHALL 維護 channels 資料表，儲存頻道識別資訊與元資料。

#### Scenario: 資料表欄位定義

- **WHEN** 資料庫初始化
- **THEN** channels 表包含以下欄位：
  - `id` SERIAL PRIMARY KEY
  - `channel_id` VARCHAR(24) UNIQUE NOT NULL（YouTube 頻道識別碼）
  - `channel_url` VARCHAR NOT NULL（使用者輸入的原始網址）
  - `channel_name` VARCHAR NULLABLE（頻道名稱）
  - `subscriber_count` INTEGER NULLABLE（訂閱數）
  - `video_count` INTEGER NULLABLE（影片數）
