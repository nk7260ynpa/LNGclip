## ADDED Requirements

### Requirement: 抓取頻道最新影片

系統 SHALL 使用 yt-dlp 從頻道 /videos 分頁抓取最新 30 部影片的資訊。

#### Scenario: 正常抓取

- **WHEN** 系統對某頻道執行影片抓取
- **THEN** 取得最新 30 部影片的 video_id、標題、縮圖、發佈時間，並以 video_id 去重後寫入 videos 表

#### Scenario: 頻道影片不足 30 部

- **WHEN** 頻道的一般影片少於 30 部
- **THEN** 抓取所有可取得的影片

#### Scenario: 抓取失敗

- **WHEN** yt-dlp 無法解析頻道影片列表
- **THEN** 記錄 WARNING 日誌，不中斷流程，回傳 0
