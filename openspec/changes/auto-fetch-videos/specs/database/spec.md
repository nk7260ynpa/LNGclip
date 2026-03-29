## MODIFIED Requirements

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
