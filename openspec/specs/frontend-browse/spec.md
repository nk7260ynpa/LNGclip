## ADDED Requirements

### Requirement: 首頁影片展示

前台 SHALL 在首頁以 3x2 網格展示 YouTube 嵌入式影片，所有頻道影片混合依發佈時間由新到舊排列。

#### Scenario: 正常載入

- **WHEN** 使用者進入首頁 `/`
- **THEN** 頁面以 3 欄 2 列的網格顯示最新 6 部影片，每格為 YouTube 嵌入式播放器（iframe），影片標題顯示在播放器下方

#### Scenario: 分頁瀏覽

- **WHEN** 使用者點擊「下一頁」
- **THEN** 顯示接下來的 6 部影片

#### Scenario: 無影片

- **WHEN** 資料庫中無任何影片
- **THEN** 頁面顯示「尚無影片」提示

#### Scenario: RWD 響應式

- **WHEN** 螢幕寬度較小（平板或手機）
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
