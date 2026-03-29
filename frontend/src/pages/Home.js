import { useState, useEffect } from 'react';
import { getChannels } from '../services/api';

function Home() {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getChannels()
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
          <div key={ch.id} className="card">
            <div className="card-body">
              <h3>{ch.channel_id}</h3>
              <p>
                <a href={ch.channel_url} target="_blank" rel="noopener noreferrer">
                  前往 YouTube 頻道
                </a>
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
