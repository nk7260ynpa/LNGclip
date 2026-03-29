## ADDED Requirements

### Requirement: 定時排程抓取

系統 SHALL 使用 APScheduler 每日在指定時間自動抓取所有啟用頻道的最新影片。

#### Scenario: 每日定時執行

- **WHEN** 系統時間到達設定的排程時間（預設每日 06:00）
- **THEN** 系統遍歷所有 `is_active=true` 的頻道，逐一抓取 RSS Feed

#### Scenario: 排程時間可設定

- **WHEN** 環境變數 `SYNC_SCHEDULE_HOUR` 與 `SYNC_SCHEDULE_MINUTE` 已設定
- **THEN** 排程依設定值執行，而非預設的 06:00

### Requirement: RSS Feed 解析

系統 SHALL 透過 YouTube RSS Feed 取得頻道最新影片資訊。

#### Scenario: 正常抓取

- **WHEN** 系統對某頻道發送 RSS 請求 `https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}`
- **THEN** 解析回傳的 XML，取得每部影片的 video_id、標題、縮圖網址、發佈時間

#### Scenario: RSS 請求失敗

- **WHEN** RSS 請求逾時或回傳錯誤
- **THEN** 系統記錄 ERROR 日誌，跳過該頻道並繼續處理下一個頻道

### Requirement: 影片去重寫入

系統 SHALL 以 video_id 為唯一鍵，僅寫入資料庫中不存在的新影片。

#### Scenario: 發現新影片

- **WHEN** RSS 回傳的影片 video_id 不存在於 videos 表
- **THEN** 將該影片寫入資料庫

#### Scenario: 影片已存在

- **WHEN** RSS 回傳的影片 video_id 已存在於 videos 表
- **THEN** 跳過該影片，不做任何更新

### Requirement: 同步日誌記錄

系統 SHALL 記錄每次同步的執行過程與結果。

#### Scenario: 同步完成

- **WHEN** 一輪同步作業完成
- **THEN** 記錄 INFO 日誌，包含：處理的頻道數、新增的影片數、總耗時
