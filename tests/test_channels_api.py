"""頻道 CRUD API 單元測試。"""

from unittest.mock import patch


SAMPLE_CHANNEL = {
    "channel_id": "UCtest123456789012345",
    "channel_name": "測試精華頻道",
    "streamer": "LNG",
    "description": "測試用頻道",
}


class TestChannelsCRUD:
    """頻道 CRUD 測試。"""

    @patch("src.api.channels.sync_channel_videos", return_value=0)
    def test_create_channel(self, mock_sync, client):
        """新增頻道應回傳 201。"""
        res = client.post("/api/channels", json=SAMPLE_CHANNEL)
        assert res.status_code == 201
        data = res.json()
        assert data["channel_name"] == "測試精華頻道"
        assert data["channel_id"] == "UCtest123456789012345"
        assert data["is_active"] is True

    @patch("src.api.channels.sync_channel_videos", return_value=0)
    def test_create_duplicate_channel(self, mock_sync, client):
        """重複 channel_id 應回傳 409。"""
        client.post("/api/channels", json=SAMPLE_CHANNEL)
        res = client.post("/api/channels", json=SAMPLE_CHANNEL)
        assert res.status_code == 409

    @patch("src.api.channels.sync_channel_videos", return_value=0)
    def test_list_channels(self, mock_sync, client):
        """列出所有頻道。"""
        client.post("/api/channels", json=SAMPLE_CHANNEL)
        res = client.get("/api/channels")
        assert res.status_code == 200
        assert len(res.json()) == 1

    @patch("src.api.channels.sync_channel_videos", return_value=0)
    def test_list_active_only(self, mock_sync, client):
        """僅列出啟用頻道。"""
        client.post("/api/channels", json=SAMPLE_CHANNEL)
        res = client.get("/api/channels?active_only=true")
        assert res.status_code == 200
        assert len(res.json()) == 1

    @patch("src.api.channels.sync_channel_videos", return_value=0)
    def test_get_channel(self, mock_sync, client):
        """取得單一頻道。"""
        create_res = client.post("/api/channels", json=SAMPLE_CHANNEL)
        ch_id = create_res.json()["id"]
        res = client.get(f"/api/channels/{ch_id}")
        assert res.status_code == 200
        assert res.json()["channel_name"] == "測試精華頻道"

    def test_get_nonexistent_channel(self, client):
        """取得不存在的頻道應回傳 404。"""
        res = client.get("/api/channels/999")
        assert res.status_code == 404

    @patch("src.api.channels.sync_channel_videos", return_value=0)
    def test_update_channel(self, mock_sync, client):
        """更新頻道資訊。"""
        create_res = client.post("/api/channels", json=SAMPLE_CHANNEL)
        ch_id = create_res.json()["id"]
        res = client.put(
            f"/api/channels/{ch_id}",
            json={"channel_name": "更新後的名稱"},
        )
        assert res.status_code == 200
        assert res.json()["channel_name"] == "更新後的名稱"

    @patch("src.api.channels.sync_channel_videos", return_value=0)
    def test_delete_channel(self, mock_sync, client):
        """刪除頻道。"""
        create_res = client.post("/api/channels", json=SAMPLE_CHANNEL)
        ch_id = create_res.json()["id"]
        res = client.delete(f"/api/channels/{ch_id}")
        assert res.status_code == 204
        res = client.get(f"/api/channels/{ch_id}")
        assert res.status_code == 404

    @patch("src.api.channels.sync_channel_videos", return_value=0)
    def test_toggle_channel(self, mock_sync, client):
        """切換頻道啟用狀態。"""
        create_res = client.post("/api/channels", json=SAMPLE_CHANNEL)
        ch_id = create_res.json()["id"]
        res = client.patch(f"/api/channels/{ch_id}/toggle")
        assert res.status_code == 200
        assert res.json()["is_active"] is False
