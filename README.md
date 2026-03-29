# LNGclip

LNG 精華影片頻道管理平台。透過後台管理 YouTube 精華頻道，前台自動展示各頻道最新影片。

## 功能

- 前台：瀏覽所有啟用的精華頻道及其最新影片
- 後台：新增、編輯、刪除、啟用/停用頻道
- 每日自動透過 YouTube RSS Feed 同步各頻道最新影片
- 手動觸發單一或全部頻道同步

## 專案架構

```text
LNGclip/
├── frontend/                 # React 前端
│   ├── src/
│   │   ├── pages/            # 頁面元件（Home, ChannelDetail, Admin）
│   │   ├── services/         # API 呼叫封裝
│   │   └── App.js            # 路由設定
│   ├── nginx.conf            # nginx 反向代理設定
│   ├── Dockerfile            # 多階段建置（Node + nginx）
│   └── package.json
├── src/                      # FastAPI 後端
│   ├── api/                  # API routes（channels, videos, sync）
│   ├── models/               # SQLAlchemy models（Channel, Video）
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # 業務邏輯（RSS 同步、排程器）
│   ├── config.py             # 環境變數設定
│   ├── logging_config.py     # 日誌設定
│   └── main.py               # FastAPI 入口
├── tests/                    # 單元測試與整合測試
├── docker/
│   ├── Dockerfile            # 後端 Dockerfile
│   ├── docker-compose.yaml   # 三個 container 編排
│   └── build.sh              # 建置腳本
├── logs/                     # 日誌目錄
├── run.sh                    # 一鍵啟動腳本
└── requirements.txt          # Python 依賴
```

## 快速開始

### 前置需求

- Docker 與 Docker Compose

### 啟動服務

```bash
./run.sh
```

啟動後可透過以下網址存取：

- 前台：<http://localhost:3000>
- 後台管理：<http://localhost:3000/admin>
- API 文件：<http://localhost:8000/docs>

### 停止服務

```bash
docker compose -f docker/docker-compose.yaml down
```

## 環境變數

| 變數 | 說明 | 預設值 |
|---|---|---|
| `DATABASE_URL` | PostgreSQL 連線字串 | `postgresql://lngclip:lngclip@postgres:5432/lngclip` |
| `SYNC_SCHEDULE_HOUR` | 每日同步小時 | `6` |
| `SYNC_SCHEDULE_MINUTE` | 每日同步分鐘 | `0` |

## 測試

### 單元測試（在 Docker container 中執行）

```bash
docker compose -f docker/docker-compose.yaml exec backend \
  python -m pytest tests/ -v
```

### 整合測試

```bash
./tests/test_docker_integration.sh
```

## API 端點

| 方法 | 路徑 | 說明 |
|---|---|---|
| GET | `/api/channels` | 取得頻道列表（`?active_only=true`） |
| GET | `/api/channels/{id}` | 取得單一頻道 |
| POST | `/api/channels` | 新增頻道 |
| PUT | `/api/channels/{id}` | 更新頻道 |
| DELETE | `/api/channels/{id}` | 刪除頻道 |
| PATCH | `/api/channels/{id}/toggle` | 切換啟用狀態 |
| GET | `/api/channels/{id}/videos` | 取得頻道影片 |
| POST | `/api/channels/{id}/sync` | 同步單一頻道 |
| POST | `/api/sync` | 同步所有頻道 |
| GET | `/api/health` | 健康檢查 |

## 授權

Apache License 2.0
