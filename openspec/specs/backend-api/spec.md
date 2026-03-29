## ADDED Requirements

### Requirement: 頻道 CRUD API

後端 SHALL 提供簡化的頻道 API。

#### Scenario: 取得所有頻道

- **WHEN** 前端發送 `GET /api/channels`
- **THEN** 回傳所有頻道列表（id、channel_id、channel_url、channel_name、subscriber_count、video_count）

#### Scenario: 新增頻道

- **WHEN** 前端發送 `POST /api/channels` 包含 `url` 欄位
- **THEN** 系統解析 URL、建立記錄、自動抓取元資料並更新 channel_name、subscriber_count、video_count

#### Scenario: 新增但抓取失敗

- **WHEN** 前端發送 `POST /api/channels` 且元資料抓取失敗
- **THEN** 仍建立頻道記錄（新欄位為 NULL），回傳 201

#### Scenario: 新增頻道 URL 無效

- **WHEN** 前端發送的 URL 無法解析出 channel_id
- **THEN** 回傳 400 錯誤，包含支援的 URL 格式說明

#### Scenario: 刪除頻道

- **WHEN** 前端發送 `DELETE /api/channels/{id}`
- **THEN** 系統刪除該頻道及其所有影片記錄，回傳 204

### Requirement: 單一頻道元資料抓取 API

後端 SHALL 提供手動觸發單一頻道元資料抓取的 API。

#### Scenario: 手動抓取

- **WHEN** 前端發送 `POST /api/channels/{id}/fetch-metadata`
- **THEN** 系統抓取該頻道元資料並更新 DB，回傳更新後的頻道資料

### Requirement: Backfill API

後端 SHALL 提供批次補足缺失元資料的 API。

#### Scenario: 補足所有缺失

- **WHEN** 前端發送 `POST /api/channels/backfill`
- **THEN** 系統遍歷所有 channel_name 為 NULL 的頻道，逐一抓取並更新
