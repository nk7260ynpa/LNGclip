## MODIFIED Requirements

### Requirement: 資料持久化

系統 SHALL 使用本地目錄掛載持久化 PostgreSQL 資料與影片縮圖。

#### Scenario: PostgreSQL 資料掛載

- **WHEN** Docker Compose 啟動 postgres 服務
- **THEN** 資料掛載至專案目錄的 `database/` 資料夾

#### Scenario: images 目錄掛載

- **WHEN** Docker Compose 啟動 backend 服務
- **THEN** `images/` 資料夾掛載至 backend container

#### Scenario: 重新啟動不遺失資料

- **WHEN** 執行 `docker compose down` 後再 `docker compose up`
- **THEN** PostgreSQL 資料透過 `database/` 目錄保留，不會遺失
