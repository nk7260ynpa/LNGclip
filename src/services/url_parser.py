"""YouTube URL 解析服務。"""

import re


def parse_channel_id(url: str) -> str:
    """從 YouTube 頻道網址解析出 channel_id。

    支援格式：
    - https://www.youtube.com/channel/UCxxxxxxx
    - https://youtube.com/channel/UCxxxxxxx

    Args:
        url: YouTube 頻道網址。

    Returns:
        channel_id 字串。

    Raises:
        ValueError: 無法解析出 channel_id。
    """
    pattern = r"(?:https?://)?(?:www\.)?youtube\.com/channel/(UC[\w-]+)"
    match = re.match(pattern, url.strip())
    if not match:
        raise ValueError(
            "無法解析此網址，請使用 https://www.youtube.com/channel/UCxxxxxxx 格式"
        )
    return match.group(1)
