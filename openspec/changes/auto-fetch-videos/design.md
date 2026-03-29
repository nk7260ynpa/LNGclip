## Context

videos 表已存在但為空，RSS 同步已停用。需要在新增頻道時用 yt-dlp 抓取最新影片。yt-dlp 已在 fetch-channel-metadata change 中引入。

## Goals / Non-Goals

**Goals:**

- video_id 放寬為 VARCHAR(32)
- 新增頻道時自動抓取最新 30 部影片
- 影片資料寫入 videos 表（去重）

**Non-Goals:**

- 定時自動更新影片列表（之後再做）
- 抓取 Shorts（僅抓取一般影片 /videos 分頁）
- 影片觀看次數、時長等額外資訊

## Decisions

### 1. 使用 yt-dlp extract_flat 抓取影片列表

```python
opts = {"quiet": True, "extract_flat": True, "playlistend": 30}
with yt_dlp.YoutubeDL(opts) as ydl:
    info = ydl.extract_info(f"{channel_url}/videos", download=False)
    for entry in info["entries"]:
        # entry["id"] → video_id
        # entry["title"] → 標題
        # entry.get("thumbnails") → 縮圖
```

使用 `playlistend: 30` 限制只抓最新 30 部，避免大量頻道耗時過久。

**替代方案**：RSS Feed 只能拿 15 部且資訊有限，yt-dlp 更靈活。

### 2. 發佈時間的取得

`extract_flat` 模式下 entry 可能不包含 `upload_date`。若無法取得，`published_at` 設為 NULL。

### 3. 抓取失敗不阻擋頻道建立

與元資料抓取相同策略，影片抓取失敗仍保留頻道記錄，記錄 WARNING 日誌。

### 4. 縮圖 URL 格式

使用標準 YouTube 縮圖 URL：`https://i.ytimg.com/vi/{video_id}/mqdefault.jpg`

## Risks / Trade-offs

- **抓取速度** → 30 部影片約 3-8 秒，加上元資料抓取，新增頻道總共約 10-15 秒。可接受。
- **DB 重建** → video_id 長度變更需重建 DB（開發階段無正式資料）
