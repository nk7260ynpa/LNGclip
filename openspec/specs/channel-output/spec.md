## ADDED Requirements

### Requirement: 頻道與影片展示

系統 SHALL 透過前端網頁展示頻道與影片資料。

#### Scenario: 前台頁面展示

- **WHEN** 使用者瀏覽前台網頁
- **THEN** 以卡片式 UI 展示頻道列表與影片列表

#### Scenario: API JSON 回應

- **WHEN** 前端呼叫後端 API
- **THEN** API 以 JSON 格式回傳資料

### Requirement: 日誌記錄

系統 SHALL 使用 Python logging 套件記錄後端執行過程。

#### Scenario: 日誌內容

- **WHEN** 後端處理 API 請求或執行排程任務
- **THEN** 記錄 INFO 級別日誌，包含：請求路徑、同步開始/完成、影片新增數等事件

#### Scenario: 錯誤記錄

- **WHEN** 執行過程中發生錯誤（RSS 抓取失敗、資料庫寫入失敗等）
- **THEN** 記錄 ERROR 級別日誌，包含錯誤原因與上下文
