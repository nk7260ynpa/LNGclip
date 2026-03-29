## ADDED Requirements

### Requirement: 首頁影片展示

前台 SHALL 在首頁以 3x3 網格展示影片縮圖，最新上傳的排最前，支援標題搜尋。

#### Scenario: 正常載入

- **WHEN** 使用者進入首頁 `/`
- **THEN** 頁面以 3 欄 3 列的網格顯示最新 9 部影片的縮圖

#### Scenario: 點擊影片

- **WHEN** 使用者點擊某影片的縮圖或標題
- **THEN** 開啟新分頁導向該影片的 YouTube 頁面（`https://www.youtube.com/watch?v={video_id}`）

#### Scenario: 搜尋影片

- **WHEN** 使用者在搜尋列輸入關鍵字並送出
- **THEN** 頁面顯示標題包含該關鍵字的影片，重置到第 1 頁

#### Scenario: 清空搜尋

- **WHEN** 使用者清空搜尋列並送出
- **THEN** 恢復顯示所有影片

#### Scenario: 搜尋無結果

- **WHEN** 搜尋關鍵字無匹配影片
- **THEN** 頁面顯示「找不到符合的影片」提示

#### Scenario: 分頁瀏覽

- **WHEN** 使用者點擊「下一頁」
- **THEN** 顯示接下來的 9 部影片

#### Scenario: 無影片

- **WHEN** 資料庫中無任何影片
- **THEN** 頁面顯示「尚無影片」提示

#### Scenario: RWD 響應式

- **WHEN** 螢幕寬度較小
- **THEN** 網格自動調整為 2 欄或 1 欄

### Requirement: 頻道影片頁面

前台 SHALL 提供頻道詳細頁面，展示該頻道的基本資訊與最新影片列表。

#### Scenario: 檢視頻道影片

- **WHEN** 使用者點擊某頻道卡片，進入 `/channel/:id`
- **THEN** 頁面顯示該頻道名稱、說明、頭像，以及依發佈時間倒序排列的影片列表

#### Scenario: 影片卡片內容

- **WHEN** 影片列表載入完成
- **THEN** 每張影片卡片包含縮圖、標題、發佈日期，點擊後開啟新分頁導向 YouTube 影片頁面

#### Scenario: 頻道無影片

- **WHEN** 該頻道尚無任何影片資料
- **THEN** 頁面顯示「尚無影片，等待下次同步」提示訊息
