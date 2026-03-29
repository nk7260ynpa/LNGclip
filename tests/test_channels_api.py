"""頻道 API 單元測試。"""

from unittest.mock import patch

SAMPLE_URL = "https://www.youtube.com/@Sunzusa_"
SAMPLE_URL_CHANNEL = "https://www.youtube.com/channel/UCtest123456789012345"
MOCK_METADATA = {
    "channel_name": "測試頻道",
    "subscriber_count": 12345,
    "video_count": 100,
}


class TestChannelsAPI:
    """頻道 API 測試。"""

    @patch("src.api.channels.fetch_channel_metadata", return_value=MOCK_METADATA)
    def test_create_channel_with_metadata(self, mock_fetch, client):
        """新增頻道應自動抓取元資料。"""
        res = client.post("/api/channels", json={"url": SAMPLE_URL})
        assert res.status_code == 201
        data = res.json()
        assert data["channel_id"] == "@Sunzusa_"
        assert data["channel_name"] == "測試頻道"
        assert data["subscriber_count"] == 12345
        assert data["video_count"] == 100

    @patch("src.api.channels.fetch_channel_metadata", return_value=None)
    def test_create_channel_metadata_fail(self, mock_fetch, client):
        """元資料抓取失敗仍應建立頻道。"""
        res = client.post("/api/channels", json={"url": SAMPLE_URL})
        assert res.status_code == 201
        data = res.json()
        assert data["channel_id"] == "@Sunzusa_"
        assert data["channel_name"] is None

    @patch("src.api.channels.fetch_channel_metadata", return_value=MOCK_METADATA)
    def test_create_duplicate_channel(self, mock_fetch, client):
        """重複頻道應回傳 409。"""
        client.post("/api/channels", json={"url": SAMPLE_URL})
        res = client.post("/api/channels", json={"url": SAMPLE_URL})
        assert res.status_code == 409

    def test_create_invalid_url(self, client):
        """無效 URL 應回傳 400。"""
        res = client.post(
            "/api/channels",
            json={"url": "https://www.google.com"},
        )
        assert res.status_code == 400

    @patch("src.api.channels.fetch_channel_metadata", return_value=MOCK_METADATA)
    def test_list_channels(self, mock_fetch, client):
        """列出所有頻道。"""
        client.post("/api/channels", json={"url": SAMPLE_URL})
        res = client.get("/api/channels")
        assert res.status_code == 200
        assert len(res.json()) == 1

    @patch("src.api.channels.fetch_channel_metadata", return_value=MOCK_METADATA)
    def test_fetch_metadata(self, mock_fetch, client):
        """手動抓取元資料。"""
        create_res = client.post("/api/channels", json={"url": SAMPLE_URL_CHANNEL})
        ch_id = create_res.json()["id"]
        res = client.post(f"/api/channels/{ch_id}/fetch-metadata")
        assert res.status_code == 200
        assert res.json()["channel_name"] == "測試頻道"

    @patch("src.api.channels.fetch_channel_metadata", return_value=MOCK_METADATA)
    def test_backfill(self, mock_fetch, client):
        """Backfill 應補足缺失元資料。"""
        # 先建立一個 metadata 為 None 的頻道
        mock_fetch.return_value = None
        client.post("/api/channels", json={"url": SAMPLE_URL})

        # backfill 時恢復正常回傳
        mock_fetch.return_value = MOCK_METADATA
        res = client.post("/api/channels/backfill")
        assert res.status_code == 200
        assert res.json()["total"] == 1
        assert res.json()["success"] == 1

    @patch("src.api.channels.fetch_channel_metadata", return_value=MOCK_METADATA)
    def test_delete_channel(self, mock_fetch, client):
        """刪除頻道。"""
        create_res = client.post("/api/channels", json={"url": SAMPLE_URL})
        ch_id = create_res.json()["id"]
        res = client.delete(f"/api/channels/{ch_id}")
        assert res.status_code == 204

    def test_delete_nonexistent_channel(self, client):
        """刪除不存在的頻道應回傳 404。"""
        res = client.delete("/api/channels/999")
        assert res.status_code == 404
