## ADDED Requirements

### Requirement: nginx API 代理 timeout

nginx SHALL 設定足夠的 proxy timeout，避免長時間 API 請求被中斷。

#### Scenario: 爬蟲 API 不 timeout

- **WHEN** 前端透過 nginx 呼叫 POST /api/crawl（耗時 3-4 分鐘）
- **THEN** nginx 等待最長 300 秒，不回傳 504
