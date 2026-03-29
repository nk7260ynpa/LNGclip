import { useState, useEffect, useCallback } from 'react';
import {
  getChannels,
  createChannel,
  deleteChannel,
  fetchMetadata,
  backfillChannels,
} from '../services/api';

function Admin() {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const loadChannels = useCallback(() => {
    getChannels()
      .then(setChannels)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadChannels();
  }, [loadChannels]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await createChannel({ url });
      setShowModal(false);
      setUrl('');
      loadChannels();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`確定要刪除頻道「${name || id}」嗎？`)) return;
    try {
      await deleteChannel(id);
      loadChannels();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleFetchMetadata = async (id) => {
    try {
      await fetchMetadata(id);
      loadChannels();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleBackfill = async () => {
    try {
      const result = await backfillChannels();
      alert(`Backfill 完成：${result.success}/${result.total} 成功`);
      loadChannels();
    } catch (err) {
      alert(err.message);
    }
  };

  const formatCount = (count) => {
    if (count == null) return '-';
    if (count >= 10000) return `${(count / 10000).toFixed(1)} 萬`;
    return count.toLocaleString();
  };

  if (loading) return <div className="empty-state">載入中...</div>;

  const hasMissing = channels.some((ch) => !ch.channel_name);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2>頻道管理</h2>
        <div>
          {hasMissing && (
            <button className="btn btn-secondary" onClick={handleBackfill}>
              補足資料
            </button>
          )}
          <button className="btn btn-primary" onClick={() => { setError(''); setUrl(''); setShowModal(true); }}>
            新增頻道
          </button>
        </div>
      </div>

      {channels.length === 0 ? (
        <div className="empty-state">尚無頻道，點擊「新增頻道」開始</div>
      ) : (
        <table className="admin-table">
          <thead>
            <tr>
              <th>頻道名稱</th>
              <th>Channel ID</th>
              <th>訂閱數</th>
              <th>影片數</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {channels.map((ch) => (
              <tr key={ch.id}>
                <td>{ch.channel_name || <span style={{ color: '#999' }}>未取得</span>}</td>
                <td>
                  <a href={ch.channel_url} target="_blank" rel="noopener noreferrer">
                    {ch.channel_id}
                  </a>
                </td>
                <td>{formatCount(ch.subscriber_count)}</td>
                <td>{formatCount(ch.video_count)}</td>
                <td>
                  {!ch.channel_name && (
                    <button className="btn btn-secondary" onClick={() => handleFetchMetadata(ch.id)}>
                      抓取
                    </button>
                  )}
                  <button
                    className="btn btn-danger"
                    onClick={() => handleDelete(ch.id, ch.channel_name || ch.channel_id)}
                  >
                    刪除
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>新增頻道</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>YouTube 頻道網址</label>
                <input
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  required
                  placeholder="https://www.youtube.com/@handle"
                />
              </div>
              <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  取消
                </button>
                <button type="submit" className="btn btn-primary">
                  新增
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Admin;
