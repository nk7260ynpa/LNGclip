## ADDED Requirements

### Requirement: 頻道清單篩選

系統 SHALL 對蒐集到的頻道進行篩選，排除無關或低品質的頻道。

#### Scenario: 依據頻道名稱篩選

- **WHEN** 系統取得搜尋結果
- **THEN** 僅保留頻道名稱中包含「LNG」關鍵字的頻道

#### Scenario: 依據活躍度篩選

- **WHEN** 系統取得頻道詳細資訊
- **THEN** 排除超過 6 個月未發佈影片的頻道（可透過設定調整門檻）

### Requirement: 頻道清單排序

系統 SHALL 依據指定欄位對頻道清單進行排序。

#### Scenario: 預設排序

- **WHEN** 未指定排序方式
- **THEN** 依訂閱數由高到低排序

#### Scenario: 自訂排序

- **WHEN** 使用者指定排序欄位（訂閱數、影片數、最新更新時間）
- **THEN** 依指定欄位與方向排序

### Requirement: 頻道去重

系統 SHALL 確保輸出清單中不包含重複頻道。

#### Scenario: 多關鍵字搜尋產生重複結果

- **WHEN** 不同關鍵字搜尋回傳相同頻道
- **THEN** 依據頻道 ID 去重，僅保留一筆
