## Context

前台目前用 iframe 嵌入 YouTube 影片（6 個 iframe 同時載入很慢）。PostgreSQL 資料存在 Docker named volume，不在專案目錄內。

## Goals / Non-Goals

**Goals:**

- 前台改為縮圖 + YouTube 超連結
- 建立 images/ 和 database/ 本地目錄
- PostgreSQL 掛載至 database/ 目錄
- 確認資料完整後刪除舊 named volume

**Non-Goals:**

- 縮圖下載到本地（先用 YouTube CDN 的縮圖 URL）
- 資料庫備份自動化

## Decisions

### 1. 縮圖用 YouTube CDN URL

直接使用 `https://i.ytimg.com/vi/{video_id}/mqdefault.jpg`，不下載到本地。images/ 資料夾預留給未來本地快取用。

### 2. 本地目錄取代 named volume

```yaml
# 舊
volumes:
  - pgdata:/var/lib/postgresql/data

# 新
volumes:
  - ../database:/var/lib/postgresql/data
```

好處：資料在專案目錄內，可直接備份。

### 3. 搬移流程

1. 停止服務
2. 將 named volume 資料複製到 database/ 目錄
3. 修改 docker-compose.yaml
4. 啟動服務，驗證資料完整
5. 刪除舊 named volume

### 4. .gitignore 排除

```
database/*
!database/.gitkeep
images/*
!images/.gitkeep
```

## Risks / Trade-offs

- **權限問題** → PostgreSQL container 以 postgres 使用者運行，bind mount 可能有權限問題。需確保 database/ 目錄權限正確。
- **images/ 暫時為空** → 目前縮圖直接用 YouTube CDN，images/ 預留未來使用。
