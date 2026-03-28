## ADDED Requirements

### Requirement: JSON 格式輸出

系統 SHALL 將最終頻道清單以 JSON 格式輸出至檔案。

#### Scenario: 正常輸出

- **WHEN** 頻道清單處理完成
- **THEN** 輸出 JSON 檔案，包含以下欄位：
  - `channel_id`：頻道 ID
  - `channel_name`：頻道名稱
  - `description`：頻道說明
  - `subscriber_count`：訂閱數
  - `video_count`：影片總數
  - `created_at`：頻道建立日期
  - `latest_video_at`：最新影片發佈時間
  - `channel_url`：頻道連結

#### Scenario: 輸出路徑可設定

- **WHEN** 使用者指定輸出路徑
- **THEN** JSON 檔案寫入指定路徑
- **WHEN** 未指定輸出路徑
- **THEN** JSON 檔案寫入預設路徑 `output/channels.json`

### Requirement: 終端機摘要輸出

系統 SHALL 在執行完成後於終端機印出摘要資訊。

#### Scenario: 正常執行完成

- **WHEN** 頻道清單輸出完成
- **THEN** 終端機顯示：找到的頻道數量、輸出檔案路徑、執行耗時

### Requirement: 日誌記錄

系統 SHALL 使用 Python logging 套件記錄執行過程。

#### Scenario: 日誌內容

- **WHEN** 系統執行任意階段
- **THEN** 記錄 INFO 級別日誌，包含：開始搜尋、找到頻道數、篩選結果、輸出完成等關鍵事件

#### Scenario: 錯誤記錄

- **WHEN** 執行過程中發生錯誤（API 呼叫失敗、檔案寫入失敗等）
- **THEN** 記錄 ERROR 級別日誌，包含錯誤原因與上下文
