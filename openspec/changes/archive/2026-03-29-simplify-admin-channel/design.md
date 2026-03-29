## Context

目前後台新增頻道需手動填入 5 個欄位，且 channels 表包含 10 個欄位。使用者希望簡化為只貼網址即可，其餘資訊之後再規劃。同時暫時停用前台展示與 RSS 排程同步，聚焦在後台管理功能。

## Goals / Non-Goals

**Goals:**

- 簡化 channels 表為 3 個欄位（id、channel_id、channel_url）
- 後台只需貼 YouTube 頻道網址即可新增
- 後端自動從 URL 解析 channel_id
- 移除新增時的 RSS 同步觸發

**Non-Goals:**

- 頻道名稱、說明、頭像等資訊的自動提取（之後再做）
- 前台頁面的重新設計（之後再做）
- RSS 排程同步功能（之後再做）

## Decisions

### 1. URL 解析邏輯放在後端

在後端 Python 實作 URL 解析，支援以下格式：
- `https://www.youtube.com/channel/UCxxxxxxx` → 直接取 channel_id
- `https://www.youtube.com/@handle` → 暫不支援（無法不透過 API 解析為 channel_id）
- `https://youtube.com/channel/UCxxxxxxx` → 同上，去除 www

**替代方案**：前端 JavaScript 解析 — 但後端統一驗證更安全。

### 2. 資料庫破壞性遷移

直接 drop 舊 channels 表並重建，因為：
- 專案仍在開發階段，無正式資料需要保留
- 3 個欄位與舊 schema 差異太大，migration 不值得

**替代方案**：Alembic migration — 過度設計，資料不需保留。

### 3. 暫時停用前台與排程

- `src/main.py` 移除排程器啟動與 sync API router
- 前台暫時顯示 channel_id 清單（無頻道名稱）
- 保留前台路由結構，之後再補內容

### 4. Videos 表暫時保留但清空

Videos 表結構不動，但因 channels 表重建會 cascade 刪除所有影片。排程停用後也不會有新影片寫入。

## Risks / Trade-offs

- **資料遺失** → 可接受，開發階段無正式資料
- **`@handle` 格式不支援** → 提示使用者改用 channel URL 格式，之後可透過 YouTube API 支援
- **前台暫時功能不完整** → 可接受，先聚焦後台
