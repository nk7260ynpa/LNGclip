"""RSS 同步服務單元測試。

目前 RSS 同步功能暫時停用，測試暫時跳過。
"""

import pytest


@pytest.mark.skip(reason="RSS 同步功能暫時停用")
class TestFetchRssFeed:
    """RSS Feed 抓取測試（暫時停用）。"""

    def test_placeholder(self):
        pass


@pytest.mark.skip(reason="RSS 同步功能暫時停用")
class TestSyncChannelVideos:
    """頻道影片同步測試（暫時停用）。"""

    def test_placeholder(self):
        pass
