## MODIFIED Requirements

### Requirement: 新增頻道

後端 SHALL 在新增頻道後自動抓取最新影片。

#### Scenario: 新增並抓取影片

- **WHEN** 前端發送 `POST /api/channels` 新增頻道
- **THEN** 系統建立頻道記錄、抓取元資料、抓取最新 30 部影片並寫入 videos 表

#### Scenario: 影片抓取失敗

- **WHEN** 影片抓取失敗
- **THEN** 頻道記錄仍保留，影片數為 0
