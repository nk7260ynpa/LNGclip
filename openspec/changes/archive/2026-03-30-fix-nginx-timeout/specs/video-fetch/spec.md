## MODIFIED Requirements

### Requirement: 抓取頻道最新影片

系統 SHALL 在抓取影片時同步下載縮圖至本地。

#### Scenario: 寫入影片並下載縮圖

- **WHEN** 系統抓取到新影片並寫入 DB
- **THEN** 同步下載縮圖到 images/{video_id}.jpg，thumbnail 欄位存本地路徑
