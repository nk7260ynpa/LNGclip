"""YouTube URL 解析服務。"""

import re


def parse_channel_id(url: str) -> str:
    """從 YouTube 頻道網址解析出識別碼。

    支援格式：
    - https://www.youtube.com/@handle
    - https://youtube.com/@handle
    - https://www.youtube.com/channel/UCxxxxxxx

    Args:
        url: YouTube 頻道網址。

    Returns:
        頻道識別碼（@handle 或 UCxxxxxxx）。

    Raises:
        ValueError: 無法解析出識別碼。
    """
    url = url.strip().rstrip("/")

    # @handle 格式
    handle_pattern = r"(?:https?://)?(?:www\.)?youtube\.com/(@[\w._-]+)"
    match = re.match(handle_pattern, url)
    if match:
        return match.group(1)

    # /channel/UCxxxxxxx 格式
    channel_pattern = r"(?:https?://)?(?:www\.)?youtube\.com/channel/(UC[\w-]+)"
    match = re.match(channel_pattern, url)
    if match:
        return match.group(1)

    raise ValueError(
        "無法解析此網址，請使用 https://www.youtube.com/@handle 格式"
    )
