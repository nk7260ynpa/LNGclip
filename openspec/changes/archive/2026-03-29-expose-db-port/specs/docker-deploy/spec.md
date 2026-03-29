## MODIFIED Requirements

### Requirement: Docker Compose 編排

系統 SHALL 透過 Docker Compose 統一管理 frontend、backend、postgres 三個 container。

#### Scenario: 一鍵啟動

- **WHEN** 執行 `run.sh`
- **THEN** 依序啟動 postgres → backend → frontend 三個 container，並確保健康檢查通過後才啟動依賴服務

#### Scenario: 服務埠號

- **WHEN** 所有 container 啟動完成
- **THEN** frontend 對外開放 port 3001，backend 對外開放 port 8001，postgres 對外開放 port 5433
