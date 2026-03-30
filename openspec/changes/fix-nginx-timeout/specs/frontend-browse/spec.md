## MODIFIED Requirements

### Requirement: 首頁影片展示

前台 SHALL 使用本地縮圖路徑顯示影片。

#### Scenario: 縮圖來源

- **WHEN** 影片列表載入完成
- **THEN** 每張影片的縮圖從 `/api/images/{video_id}.jpg` 讀取
