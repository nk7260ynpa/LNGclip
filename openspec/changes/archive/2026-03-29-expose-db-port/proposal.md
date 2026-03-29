## Why

PostgreSQL 目前僅限 Docker 內部網路存取，無法從本機使用 pgAdmin、DBeaver 等工具連線，不利於開發除錯。

## What Changes

- docker-compose.yaml 的 postgres 服務新增 port mapping，將容器內 5432 映射至主機 5433（避免與本機可能存在的 PostgreSQL 衝突）

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `docker-deploy`: postgres 服務新增對外 port mapping

## Impact

- `docker/docker-compose.yaml`：postgres 服務新增 ports 設定
