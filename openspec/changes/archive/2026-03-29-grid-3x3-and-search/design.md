## Context

前台目前 3x2 網格每頁 6 部影片，無搜尋功能。

## Goals / Non-Goals

**Goals:**

- 每頁 9 部影片（3x3）
- 最新上傳的排最前
- 搜尋列可依標題模糊搜尋

**Non-Goals:**

- 全文搜尋引擎（Elasticsearch 等）
- 搜尋頻道名稱（僅搜尋影片標題）

## Decisions

### 1. 後端 ILIKE 搜尋

使用 PostgreSQL ILIKE 做標題模糊搜尋：

```python
@router.get("/api/videos")
def list_videos(search: str = None):
    query = db.query(Video)
    if search:
        query = query.filter(Video.title.ilike(f"%{search}%"))
```

簡單直接，90 部影片量級不需要索引優化。

### 2. 前端搜尋 UX

搜尋列放在標題下方，輸入後按 Enter 或點搜尋按鈕觸發。搜尋時重置到第 1 頁。清空搜尋恢復全部影片。

## Risks / Trade-offs

- **ILIKE 效能** → 資料量小，無需擔心。未來資料量大時可加 GIN index。
