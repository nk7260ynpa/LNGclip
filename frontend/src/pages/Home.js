import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getChannels } from '../services/api';

function Home() {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    getChannels(true)
      .then(setChannels)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="empty-state">載入中...</div>;

  if (channels.length === 0) {
    return <div className="empty-state">尚無頻道</div>;
  }

  return (
    <div>
      <h2>LNG 精華頻道</h2>
      <div className="card-grid">
        {channels.map((ch) => (
          <div
            key={ch.id}
            className="card"
            onClick={() => navigate(`/channel/${ch.id}`)}
          >
            {ch.thumbnail && (
              <img
                src={ch.thumbnail}
                alt={ch.channel_name}
                style={{ width: '100%', height: 160, objectFit: 'cover' }}
              />
            )}
            <div className="card-body">
              <h3>{ch.channel_name}</h3>
              <p>{ch.streamer}</p>
              <p>{ch.video_count} 部影片</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
