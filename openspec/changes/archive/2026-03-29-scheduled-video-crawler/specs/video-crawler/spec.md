## ADDED Requirements

### Requirement: 定期爬蟲檢查新影片

系統 SHALL 透過獨立 crawler container 定期檢查所有頻道是否有新影片，並將新影片寫入 videos 表。

#### Scenario: 正常執行

- **WHEN** 爬蟲排程觸發
- **THEN** 系統遍歷所有頻道，抓取最新 15 部影片，以 video_id 去重後寫入 DB

#### Scenario: 頻道無新影片

- **WHEN** 某頻道的最新影片皆已存在於 DB
- **THEN** 跳過該頻道，不做任何寫入

#### Scenario: 抓取失敗

- **WHEN** 某頻道的 yt-dlp 抓取失敗
- **THEN** 記錄 WARNING 日誌，跳過該頻道並繼續處理下一個

#### Scenario: 執行完成

- **WHEN** 所有頻道處理完畢
- **THEN** 記錄 INFO 日誌，包含處理的頻道數、新增的影片數、總耗時

### Requirement: 每 3 天自動執行

系統 SHALL 使用 cron 排程每 3 天自動觸發爬蟲。

#### Scenario: 排程觸發

- **WHEN** 系統時間到達排程時間（每 3 天 06:00）
- **THEN** 自動執行爬蟲腳本
