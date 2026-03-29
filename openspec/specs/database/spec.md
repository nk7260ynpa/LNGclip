## ADDED Requirements

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

### Requirement: videos 資料表

系統 SHALL 維護 videos 資料表，儲存影片資料。

#### Scenario: 資料表欄位定義

- **WHEN** 資料庫初始化
- **THEN** videos 表包含以下欄位：
  - `id` SERIAL PRIMARY KEY
  - `channel_id` VARCHAR(24) FOREIGN KEY REFERENCES channels(channel_id) ON DELETE CASCADE
  - `video_id` VARCHAR(32) UNIQUE NOT NULL
  - `title` VARCHAR NOT NULL
  - `thumbnail` VARCHAR
  - `published_at` TIMESTAMP
  - `created_at` TIMESTAMP DEFAULT NOW()

### Requirement: 資料庫自動遷移

系統 SHALL 在啟動時自動建立或更新資料表結構。

#### Scenario: 首次啟動

- **WHEN** 後端服務首次啟動且資料表不存在
- **THEN** 系統透過 SQLAlchemy 自動建立所有資料表
