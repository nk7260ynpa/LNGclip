## ADDED Requirements

### Requirement: 抓取頻道元資料

系統 SHALL 使用 yt-dlp 從 YouTube 頻道 URL 抓取元資料。

#### Scenario: 正常抓取

- **WHEN** 系統對某頻道 URL 執行元資料抓取
- **THEN** 取得頻道名稱、訂閱數、影片數

#### Scenario: 抓取失敗

- **WHEN** yt-dlp 無法解析頻道 URL（網路錯誤或格式不支援）
- **THEN** 記錄 WARNING 日誌並回傳 None，不中斷流程
