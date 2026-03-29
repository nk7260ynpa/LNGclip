## MODIFIED Requirements

### Requirement: Docker Compose 編排

系統 SHALL 透過 Docker Compose 統一管理 frontend、backend、postgres、crawler 四個 container。

#### Scenario: 一鍵啟動

- **WHEN** 執行 `run.sh`
- **THEN** 依序啟動 postgres → backend + crawler → frontend 四個 container

#### Scenario: crawler 服務

- **WHEN** crawler container 啟動
- **THEN** crond 常駐運行，依排程每 3 天觸發爬蟲腳本
