## ADDED Requirements

### Requirement: 解析 YouTube 頻道網址

系統 SHALL 從 YouTube 頻道網址中解析出 channel_id。

#### Scenario: 標準頻道 URL

- **WHEN** 輸入 `https://www.youtube.com/channel/UCxxxxxxx`
- **THEN** 解析出 `UCxxxxxxx` 作為 channel_id

#### Scenario: 不含 www 的 URL

- **WHEN** 輸入 `https://youtube.com/channel/UCxxxxxxx`
- **THEN** 解析出 `UCxxxxxxx` 作為 channel_id

#### Scenario: 不支援的 URL 格式

- **WHEN** 輸入 `https://www.youtube.com/@handle` 或其他非 channel URL
- **THEN** 回傳錯誤，提示使用者使用 `youtube.com/channel/UCxxxxxxx` 格式
