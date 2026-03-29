## ADDED Requirements

### Requirement: channels 資料表

系統 SHALL 建立 channels 資料表，儲存 YouTube 頻道的管理資訊。

#### Scenario: 資料表欄位定義

- **WHEN** 資料庫初始化
- **THEN** channels 表包含以下欄位：
  - `id` SERIAL PRIMARY KEY
  - `channel_name` VARCHAR NOT NULL（頻道名稱）
  - `channel_id` VARCHAR(24) UNIQUE NOT NULL（YouTube 頻道 ID）
  - `channel_url` VARCHAR（頻道連結，自動由 channel_id 組成）
  - `description` TEXT（頻道說明）
  - `thumbnail` VARCHAR（頻道頭像網址）
  - `streamer` VARCHAR NOT NULL（實況主名稱）
  - `is_active` BOOLEAN DEFAULT TRUE（是否啟用）
  - `created_at` TIMESTAMP DEFAULT NOW()
  - `updated_at` TIMESTAMP DEFAULT NOW()

### Requirement: videos 資料表

系統 SHALL 建立 videos 資料表，儲存從 RSS Feed 抓取的影片資料。

#### Scenario: 資料表欄位定義

- **WHEN** 資料庫初始化
- **THEN** videos 表包含以下欄位：
  - `id` SERIAL PRIMARY KEY
  - `channel_id` INTEGER FOREIGN KEY REFERENCES channels(id) ON DELETE CASCADE
  - `video_id` VARCHAR(11) UNIQUE NOT NULL（YouTube 影片 ID）
  - `title` VARCHAR NOT NULL（影片標題）
  - `thumbnail` VARCHAR（影片縮圖網址）
  - `published_at` TIMESTAMP（影片發佈時間）
  - `created_at` TIMESTAMP DEFAULT NOW()

### Requirement: 資料庫自動遷移

系統 SHALL 在啟動時自動建立或更新資料表結構。

#### Scenario: 首次啟動

- **WHEN** 後端服務首次啟動且資料表不存在
- **THEN** 系統透過 SQLAlchemy 自動建立所有資料表
