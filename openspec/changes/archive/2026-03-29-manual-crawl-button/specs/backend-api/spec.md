## ADDED Requirements

### Requirement: 手動觸發爬蟲 API

後端 SHALL 提供手動觸發所有頻道影片爬蟲的 API。

#### Scenario: 觸發爬蟲

- **WHEN** 前端發送 `POST /api/crawl`
- **THEN** 系統遍歷所有頻道，抓取最新影片並寫入 DB，回傳處理的頻道數與新增影片數
