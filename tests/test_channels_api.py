"""頻道 API 單元測試。"""

SAMPLE_URL = "https://www.youtube.com/channel/UCtest123456789012345"


class TestChannelsAPI:
    """頻道 API 測試。"""

    def test_create_channel(self, client):
        """新增頻道應回傳 201。"""
        res = client.post("/api/channels", json={"url": SAMPLE_URL})
        assert res.status_code == 201
        data = res.json()
        assert data["channel_id"] == "UCtest123456789012345"
        assert data["channel_url"] == SAMPLE_URL

    def test_create_duplicate_channel(self, client):
        """重複 channel_id 應回傳 409。"""
        client.post("/api/channels", json={"url": SAMPLE_URL})
        res = client.post("/api/channels", json={"url": SAMPLE_URL})
        assert res.status_code == 409

    def test_create_invalid_url(self, client):
        """無效 URL 應回傳 400。"""
        res = client.post(
            "/api/channels",
            json={"url": "https://www.youtube.com/@somehandle"},
        )
        assert res.status_code == 400

    def test_list_channels(self, client):
        """列出所有頻道。"""
        client.post("/api/channels", json={"url": SAMPLE_URL})
        res = client.get("/api/channels")
        assert res.status_code == 200
        assert len(res.json()) == 1

    def test_delete_channel(self, client):
        """刪除頻道。"""
        create_res = client.post("/api/channels", json={"url": SAMPLE_URL})
        ch_id = create_res.json()["id"]
        res = client.delete(f"/api/channels/{ch_id}")
        assert res.status_code == 204

    def test_delete_nonexistent_channel(self, client):
        """刪除不存在的頻道應回傳 404。"""
        res = client.delete("/api/channels/999")
        assert res.status_code == 404
