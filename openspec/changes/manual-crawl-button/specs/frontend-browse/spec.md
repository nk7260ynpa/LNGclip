## ADDED Requirements

### Requirement: 檢查新影片按鈕

前台首頁 SHALL 提供「檢查新影片」按鈕，手動觸發爬蟲。

#### Scenario: 點擊按鈕

- **WHEN** 使用者點擊「檢查新影片」按鈕
- **THEN** 按鈕變為「檢查中...」disabled 狀態，完成後顯示結果（新增影片數）並重新載入影片列表

#### Scenario: 爬蟲執行失敗

- **WHEN** API 回傳錯誤
- **THEN** 顯示錯誤提示，按鈕恢復可點擊
