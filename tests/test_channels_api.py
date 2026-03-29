"""頻道 API 單元測試。"""

from unittest.mock import patch

SAMPLE_URL = "https://www.youtube.com/@Sunzusa_"
SAMPLE_URL_CHANNEL = "https://www.youtube.com/channel/UCtest123456789012345"
MOCK_METADATA = {
    "channel_name": "測試頻道",
    "subscriber_count": 12345,
    "video_count": 100,
}


@patch("src.api.channels.fetch_channel_videos", return_value=0)
@patch("src.api.channels.fetch_channel_metadata", return_value=MOCK_METADATA)
class TestChannelsAPI:
    """頻道 API 測試。"""

    def test_create_channel_with_metadata(self, mock_meta, mock_videos, client):
        """新增頻道應自動抓取元資料與影片。"""
        res = client.post("/api/channels", json={"url": SAMPLE_URL})
        assert res.status_code == 201
        data = res.json()
        assert data["channel_id"] == "@Sunzusa_"
        assert data["channel_name"] == "測試頻道"
        assert data["subscriber_count"] == 12345
        mock_videos.assert_called_once()

    def test_create_channel_metadata_fail(self, mock_meta, mock_videos, client):
        """元資料抓取失敗仍應建立頻道。"""
        mock_meta.return_value = None
        res = client.post("/api/channels", json={"url": SAMPLE_URL})
        assert res.status_code == 201
        assert res.json()["channel_name"] is None
        mock_videos.assert_called_once()

    def test_create_duplicate_channel(self, mock_meta, mock_videos, client):
        """重複頻道應回傳 409。"""
        client.post("/api/channels", json={"url": SAMPLE_URL})
        res = client.post("/api/channels", json={"url": SAMPLE_URL})
        assert res.status_code == 409

    def test_create_invalid_url(self, mock_meta, mock_videos, client):
        """無效 URL 應回傳 400。"""
        res = client.post(
            "/api/channels",
            json={"url": "https://www.google.com"},
        )
        assert res.status_code == 400

    def test_list_channels(self, mock_meta, mock_videos, client):
        """列出所有頻道。"""
        client.post("/api/channels", json={"url": SAMPLE_URL})
        res = client.get("/api/channels")
        assert res.status_code == 200
        assert len(res.json()) == 1

    def test_fetch_metadata(self, mock_meta, mock_videos, client):
        """手動抓取元資料。"""
        create_res = client.post("/api/channels", json={"url": SAMPLE_URL_CHANNEL})
        ch_id = create_res.json()["id"]
        res = client.post(f"/api/channels/{ch_id}/fetch-metadata")
        assert res.status_code == 200
        assert res.json()["channel_name"] == "測試頻道"

    def test_backfill(self, mock_meta, mock_videos, client):
        """Backfill 應補足缺失元資料。"""
        mock_meta.return_value = None
        client.post("/api/channels", json={"url": SAMPLE_URL})

        mock_meta.return_value = MOCK_METADATA
        res = client.post("/api/channels/backfill")
        assert res.status_code == 200
        assert res.json()["total"] == 1
        assert res.json()["success"] == 1

    def test_delete_channel(self, mock_meta, mock_videos, client):
        """刪除頻道。"""
        create_res = client.post("/api/channels", json={"url": SAMPLE_URL})
        ch_id = create_res.json()["id"]
        res = client.delete(f"/api/channels/{ch_id}")
        assert res.status_code == 204

    def test_delete_nonexistent_channel(self, mock_meta, mock_videos, client):
        """刪除不存在的頻道應回傳 404。"""
        res = client.delete("/api/channels/999")
        assert res.status_code == 404
