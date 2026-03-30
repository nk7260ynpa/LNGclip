## ADDED Requirements

### Requirement: 下載影片縮圖到本地

系統 SHALL 在抓取影片時同步下載縮圖至 images/ 目錄。

#### Scenario: 正常下載

- **WHEN** 系統抓取到新影片
- **THEN** 從 YouTube CDN 下載縮圖存為 `images/{video_id}.jpg`，thumbnail 欄位存本地路徑

#### Scenario: 下載失敗

- **WHEN** 縮圖下載失敗
- **THEN** 記錄 WARNING 日誌，thumbnail 欄位保留 YouTube CDN URL 作為 fallback
