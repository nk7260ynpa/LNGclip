## Context

前台首頁目前只有頻道 ID 列表。videos 表已有資料（每個頻道 30 部），需要在前台展示。

## Goals / Non-Goals

**Goals:**

- 前台首頁以 3x2 網格展示 YouTube 嵌入式影片
- 所有頻道影片混合，最新的排最前面
- 支援分頁瀏覽（每頁 6 部）

**Non-Goals:**

- 頻道分類篩選（之後再做）
- 影片搜尋功能

## Decisions

### 1. YouTube 嵌入式播放器

使用 YouTube iframe embed：
```html
<iframe
  src="https://www.youtube.com/embed/{video_id}"
  width="100%"
  style="aspect-ratio: 16/9"
  frameborder="0"
  allowfullscreen
/>
```

### 2. 3x2 網格佈局

使用 CSS Grid：3 欄固定，每頁 6 部影片（3x2）。RWD 時自動調整為 2 欄或 1 欄。

### 3. 全域影片 API

新增 `GET /api/videos?page=1&per_page=6`，跨頻道查詢所有影片，依 published_at DESC 排序，支援分頁。

### 4. 前端分頁

使用「上一頁 / 下一頁」按鈕分頁，不使用無限滾動，保持簡單。

## Risks / Trade-offs

- **嵌入式影片載入速度** → 6 部 iframe 同時載入可能稍慢，但可接受
- **影片無發佈時間** → published_at 為 NULL 的影片排在最後
