## MODIFIED Requirements

### Requirement: videos 資料表

系統 SHALL 維護 videos 資料表，儲存影片資料。

#### Scenario: 資料表欄位定義

- **WHEN** 資料庫初始化
- **THEN** videos 表的 `video_id` 欄位為 VARCHAR(32) UNIQUE NOT NULL
