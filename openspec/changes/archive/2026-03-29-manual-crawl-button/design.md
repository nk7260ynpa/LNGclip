## Context

爬蟲目前在獨立 crawler container 中透過 cron 每 3 天執行。需要讓 backend 也能觸發相同的爬蟲邏輯，供前端按鈕呼叫。

## Goals / Non-Goals

**Goals:**

- 後端提供 API 執行爬蟲（複用 video_fetch 邏輯）
- 前端按鈕觸發後顯示結果（新增幾部影片）
- 爬蟲執行期間按鈕顯示 loading 狀態

**Non-Goals:**

- 背景非同步執行（同步等待完成即可，頻道數少）
- 爬蟲進度即時回報

## Decisions

### 1. 後端同步執行

爬蟲邏輯直接在 API request 中同步執行，遍歷所有頻道呼叫 `fetch_channel_videos`。6 個頻道約需 2-4 分鐘（非 flat 模式），透過較長的 timeout 處理。

**替代方案**：背景任務 + 輪詢狀態 — 過度設計，頻道數少同步可接受。

### 2. 複用現有 video_fetch

直接匯入 `src/services/video_fetch.py` 的 `fetch_channel_videos`，與 crawler.py 相同邏輯。

### 3. 前端 UX

按鈕放在標題右側，點擊後切換為「檢查中...」disabled 狀態，完成後 alert 顯示結果並重新載入影片列表。

## Risks / Trade-offs

- **執行時間長** → 非 flat 模式每頻道約 30-40 秒，6 頻道約 3-4 分鐘。前端需設較長的 fetch timeout。
