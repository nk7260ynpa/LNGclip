## Context

channels 表目前僅有 id、channel_id、channel_url，缺少頻道名稱等展示用資訊。使用者不想使用 YouTube Data API（需 API Key），改用 yt-dlp 抓取頻道元資料。

## Goals / Non-Goals

**Goals:**

- channels 表新增 channel_name、subscriber_count、video_count
- 新增頻道時自動抓取元資料
- 提供 API 補足現有頻道缺失的元資料
- 後台列表顯示這些資訊

**Non-Goals:**

- 定時自動更新訂閱數/影片數（之後再做）
- 抓取頻道頭像或說明（之後再做）

## Decisions

### 1. 使用 yt-dlp 抓取元資料

使用 yt-dlp 的 Python API 從頻道 URL 提取資訊，不需要 YouTube API Key。

```python
import yt_dlp

opts = {"quiet": True, "extract_flat": True, "playlist_items": "0"}
with yt_dlp.YoutubeDL(opts) as ydl:
    info = ydl.extract_info(channel_url, download=False)
    # info["channel"] → 頻道名稱
    # info["channel_follower_count"] → 訂閱數
    # info.get("playlist_count") → 影片數
```

**替代方案**：YouTube Data API v3 — 需要 API Key，使用者不希望引入。

### 2. 新增欄位允許 NULL

三個新欄位皆允許 NULL，因為：
- 新增頻道時 yt-dlp 可能抓取失敗
- 現有頻道尚未抓取，需 backfill

### 3. 抓取失敗不阻擋新增

新增頻道時若元資料抓取失敗，仍然建立頻道記錄（欄位為 NULL），記錄 WARNING 日誌。使用者可後續透過 backfill API 重試。

### 4. Backfill API 設計

- `POST /api/channels/backfill`：遍歷所有 channel_name 為 NULL 的頻道，逐一抓取元資料
- `POST /api/channels/{id}/fetch-metadata`：抓取單一頻道的元資料

## Risks / Trade-offs

- **yt-dlp 速度** → 每次抓取約 2-5 秒，可接受（新增頻道不頻繁）
- **yt-dlp 穩定性** → YouTube 改版可能導致解析失敗，需定期更新 yt-dlp 版本
- **Docker image 變大** → yt-dlp 會增加約 20MB，可接受
