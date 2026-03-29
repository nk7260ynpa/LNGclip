## ADDED Requirements

### Requirement: 解析 YouTube 頻道網址

系統 SHALL 從 YouTube 頻道網址中解析出頻道識別碼。

#### Scenario: @handle 格式（預設）

- **WHEN** 輸入 `https://www.youtube.com/@handle`
- **THEN** 解析出 `@handle` 作為 channel_id

#### Scenario: /channel/ 格式（相容）

- **WHEN** 輸入 `https://www.youtube.com/channel/UCxxxxxxx`
- **THEN** 解析出 `UCxxxxxxx` 作為 channel_id

#### Scenario: 不含 www 的 URL

- **WHEN** 輸入 `https://youtube.com/@handle`
- **THEN** 解析出 `@handle` 作為 channel_id

#### Scenario: 不支援的 URL 格式

- **WHEN** 輸入非 YouTube 頻道網址
- **THEN** 回傳錯誤，提示使用者使用 `https://www.youtube.com/@handle` 格式
