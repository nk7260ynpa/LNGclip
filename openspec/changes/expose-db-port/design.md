## Context

開發階段需要從本機直接連線 PostgreSQL 進行除錯。

## Goals / Non-Goals

**Goals:**

- 本機可透過 `localhost:5433` 連線 PostgreSQL

**Non-Goals:**

- 正式環境的安全性設定

## Decisions

### 使用 5433 而非 5432

避免與本機可能已安裝的 PostgreSQL 衝突。

## Risks / Trade-offs

- **安全性** → 開發用途，可接受。正式部署時應移除對外映射。
