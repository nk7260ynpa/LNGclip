import { useState, useEffect, useCallback } from 'react';
import {
  getChannels,
  createChannel,
  updateChannel,
  deleteChannel,
  toggleChannel,
  syncChannel,
  syncAll,
} from '../services/api';

const EMPTY_FORM = {
  channel_id: '',
  channel_name: '',
  streamer: '',
  description: '',
  thumbnail: '',
};

function Admin() {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
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

  const openCreate = () => {
    setEditingId(null);
    setForm(EMPTY_FORM);
    setError('');
    setShowModal(true);
  };

  const openEdit = (ch) => {
    setEditingId(ch.id);
    setForm({
      channel_id: ch.channel_id,
      channel_name: ch.channel_name,
      streamer: ch.streamer,
      description: ch.description || '',
      thumbnail: ch.thumbnail || '',
    });
    setError('');
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      if (editingId) {
        const { channel_id, ...updateData } = form;
        await updateChannel(editingId, updateData);
      } else {
        await createChannel(form);
      }
      setShowModal(false);
      loadChannels();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id, name) => {
    if (!window.confirm(`確定要刪除「${name}」嗎？將一併刪除所有影片。`)) return;
    try {
      await deleteChannel(id);
      loadChannels();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleToggle = async (id) => {
    try {
      await toggleChannel(id);
      loadChannels();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleSync = async (id) => {
    try {
      const result = await syncChannel(id);
      alert(`同步完成，新增 ${result.new_videos} 部影片`);
      loadChannels();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleSyncAll = async () => {
    try {
      const result = await syncAll();
      alert(
        `同步完成：${result.channels_processed} 個頻道，新增 ${result.total_new_videos} 部影片`
      );
      loadChannels();
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div className="empty-state">載入中...</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2>頻道管理</h2>
        <div>
          <button className="btn btn-secondary" onClick={handleSyncAll}>
            同步所有頻道
          </button>
          <button className="btn btn-primary" onClick={openCreate}>
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
              <th>實況主</th>
              <th>狀態</th>
              <th>影片數</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {channels.map((ch) => (
              <tr key={ch.id}>
                <td>{ch.channel_name}</td>
                <td>{ch.streamer}</td>
                <td>
                  <span className={`badge ${ch.is_active ? 'badge-active' : 'badge-inactive'}`}>
                    {ch.is_active ? '啟用' : '停用'}
                  </span>
                </td>
                <td>{ch.video_count}</td>
                <td>
                  <button className="btn btn-secondary" onClick={() => openEdit(ch)}>
                    編輯
                  </button>
                  <button
                    className={`btn ${ch.is_active ? 'btn-secondary' : 'btn-success'}`}
                    onClick={() => handleToggle(ch.id)}
                  >
                    {ch.is_active ? '停用' : '啟用'}
                  </button>
                  <button className="btn btn-secondary" onClick={() => handleSync(ch.id)}>
                    同步
                  </button>
                  <button
                    className="btn btn-danger"
                    onClick={() => handleDelete(ch.id, ch.channel_name)}
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
            <h2>{editingId ? '編輯頻道' : '新增頻道'}</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <form onSubmit={handleSubmit}>
              {!editingId && (
                <div className="form-group">
                  <label>YouTube 頻道 ID</label>
                  <input
                    value={form.channel_id}
                    onChange={(e) => setForm({ ...form, channel_id: e.target.value })}
                    required
                    placeholder="UCxxxxxxxxxx"
                  />
                </div>
              )}
              <div className="form-group">
                <label>頻道名稱</label>
                <input
                  value={form.channel_name}
                  onChange={(e) => setForm({ ...form, channel_name: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>實況主名稱</label>
                <input
                  value={form.streamer}
                  onChange={(e) => setForm({ ...form, streamer: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>說明</label>
                <textarea
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  rows={3}
                />
              </div>
              <div className="form-group">
                <label>頻道頭像網址</label>
                <input
                  value={form.thumbnail}
                  onChange={(e) => setForm({ ...form, thumbnail: e.target.value })}
                />
              </div>
              <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>
                  取消
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingId ? '儲存' : '新增'}
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
