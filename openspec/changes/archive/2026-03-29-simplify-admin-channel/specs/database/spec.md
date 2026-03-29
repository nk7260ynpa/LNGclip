## MODIFIED Requirements

### Requirement: channels 資料表

系統 SHALL 維護簡化的 channels 資料表，僅儲存頻道識別資訊。

#### Scenario: 資料表欄位定義

- **WHEN** 資料庫初始化
- **THEN** channels 表包含以下欄位：
  - `id` SERIAL PRIMARY KEY
  - `channel_id` VARCHAR(24) UNIQUE NOT NULL（YouTube 頻道 ID）
  - `channel_url` VARCHAR NOT NULL（使用者輸入的原始網址）

## REMOVED Requirements

### Requirement: videos 資料表

**Reason**: RSS 同步暫時停用，videos 表暫無資料寫入。表結構保留但不再有新資料。
**Migration**: 之後恢復 RSS 同步時重新啟用。
