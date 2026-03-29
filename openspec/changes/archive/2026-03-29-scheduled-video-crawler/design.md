## Context

影片目前只在新增頻道時抓取。需要獨立的 crawler container 定期更新，與 backend 分離避免互相影響。

## Goals / Non-Goals

**Goals:**

- 獨立 crawler container，與 backend 共用同一份 Python 程式碼和 DB
- 每 3 天自動執行一次爬蟲
- 複用現有 video_fetch.py 的抓取邏輯
- 記錄執行日誌

**Non-Goals:**

- 即時推送通知（有新影片時）
- 爬蟲任務的 Web UI 管理

## Decisions

### 1. 獨立 container + cron 排程

crawler container 啟動後透過 cron 排程每 3 天執行爬蟲腳本。container 保持常駐（不是 one-shot），由 crond 負責定時觸發。

```
crawler container:
  啟動 → crond → 每 3 天執行 python -m src.crawler
```

**替代方案**：APScheduler 內建在 backend — 已在之前被移除，且 crawler 獨立運作更穩定。

### 2. 複用現有程式碼

crawler 共用 backend 的 `src/` 程式碼（相同 image base），直接匯入 `video_fetch.py` 和 models，不需要透過 HTTP API。

### 3. Dockerfile.crawler

基於 backend 相同的 Python 3.12-slim，安裝相同 requirements，額外安裝 cron：

```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y cron
# ... 複製程式碼、設定 crontab
CMD ["cron", "-f"]
```

### 4. Cron 排程設定

```
0 6 */3 * * cd /app && python -m src.crawler >> /app/logs/crawler.log 2>&1
```

每 3 天的 06:00 執行，日誌輸出至 `/app/logs/crawler.log`。

### 5. 爬蟲腳本邏輯

```python
# src/crawler.py
1. 連線 DB
2. 查詢所有頻道
3. 對每個頻道呼叫 fetch_channel_videos(channel, db, limit=15)
4. 記錄結果（處理頻道數、新增影片數、耗時）
5. 關閉 DB
```

limit 設為 15（只檢查最新 15 部，足以覆蓋 3 天的新影片量）。

## Risks / Trade-offs

- **cron 無法動態調整排程** → 修改需重建 container，可接受
- **crawler 與 backend 共用 DB** → 無 lock 衝突風險（INSERT 為獨立操作，video_id UNIQUE 防重複）
- **yt-dlp 限制** → 多頻道連續抓取可能觸發 YouTube 限流，每頻道間加 2 秒延遲
