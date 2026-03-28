"""RSS 同步服務單元測試。"""

from unittest.mock import patch, MagicMock
from datetime import datetime

from src.models.channel import Channel
from src.models.video import Video
from src.services.rss_sync import fetch_rss_feed, sync_channel_videos


class TestFetchRssFeed:
    """RSS Feed 抓取測試。"""

    @patch("src.services.rss_sync.feedparser.parse")
    def test_parse_feed_entries(self, mock_parse):
        """正常解析 RSS entries。"""
        mock_parse.return_value = MagicMock(
            bozo=False,
            entries=[
                {
                    "yt_videoid": "abc12345678",
                    "title": "測試影片",
                    "published_parsed": (2026, 3, 29, 12, 0, 0, 0, 0, 0),
                },
            ],
        )
        videos = fetch_rss_feed("UCtest")
        assert len(videos) == 1
        assert videos[0]["video_id"] == "abc12345678"
        assert videos[0]["title"] == "測試影片"
        assert videos[0]["published_at"] == datetime(2026, 3, 29, 12, 0, 0)

    @patch("src.services.rss_sync.feedparser.parse")
    def test_parse_error_returns_empty(self, mock_parse):
        """RSS 抓取失敗時回傳空列表。"""
        mock_parse.return_value = MagicMock(
            bozo=True,
            bozo_exception=Exception("Network error"),
            entries=[],
        )
        videos = fetch_rss_feed("UCtest")
        assert videos == []


class TestSyncChannelVideos:
    """頻道影片同步測試。"""

    @patch("src.services.rss_sync.fetch_rss_feed")
    def test_sync_new_videos(self, mock_fetch, db):
        """同步新影片應寫入資料庫。"""
        channel = Channel(
            channel_name="測試頻道",
            channel_id="UCtest",
            streamer="LNG",
        )
        db.add(channel)
        db.commit()

        mock_fetch.return_value = [
            {
                "video_id": "vid00000001",
                "title": "影片一",
                "thumbnail": "https://example.com/thumb.jpg",
                "published_at": datetime(2026, 3, 29),
            },
        ]

        new_count = sync_channel_videos(channel, db)
        assert new_count == 1

        videos = db.query(Video).filter(Video.channel_id == channel.id).all()
        assert len(videos) == 1
        assert videos[0].title == "影片一"

    @patch("src.services.rss_sync.fetch_rss_feed")
    def test_skip_existing_videos(self, mock_fetch, db):
        """已存在的影片應被跳過。"""
        channel = Channel(
            channel_name="測試頻道",
            channel_id="UCtest",
            streamer="LNG",
        )
        db.add(channel)
        db.commit()

        existing = Video(
            channel_id=channel.id,
            video_id="vid00000001",
            title="既有影片",
        )
        db.add(existing)
        db.commit()

        mock_fetch.return_value = [
            {
                "video_id": "vid00000001",
                "title": "既有影片",
                "thumbnail": "",
                "published_at": None,
            },
            {
                "video_id": "vid00000002",
                "title": "新影片",
                "thumbnail": "",
                "published_at": None,
            },
        ]

        new_count = sync_channel_videos(channel, db)
        assert new_count == 1

        total = db.query(Video).filter(Video.channel_id == channel.id).count()
        assert total == 2
