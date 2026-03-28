import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getChannel, getChannelVideos } from '../services/api';

function ChannelDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [channel, setChannel] = useState(null);
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getChannel(id), getChannelVideos(id)])
      .then(([ch, vids]) => {
        setChannel(ch);
        setVideos(vids);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="empty-state">載入中...</div>;
  if (!channel) return <div className="empty-state">頻道不存在</div>;

  return (
    <div>
      <button
        className="btn btn-secondary"
        onClick={() => navigate('/')}
        style={{ marginBottom: 16 }}
      >
        返回首頁
      </button>

      <div className="channel-header">
        <h2>{channel.channel_name}</h2>
        <p>{channel.streamer} · {channel.video_count} 部影片</p>
        {channel.description && <p>{channel.description}</p>}
      </div>

      {videos.length === 0 ? (
        <div className="empty-state">尚無影片，等待下次同步</div>
      ) : (
        <div className="video-grid">
          {videos.map((video) => (
            <div key={video.id} className="video-card">
              <a
                href={`https://www.youtube.com/watch?v=${video.video_id}`}
                target="_blank"
                rel="noopener noreferrer"
              >
                {video.thumbnail && (
                  <img src={video.thumbnail} alt={video.title} />
                )}
                <div className="card-body">
                  <h4>{video.title}</h4>
                  <p>
                    {video.published_at
                      ? new Date(video.published_at).toLocaleDateString('zh-TW')
                      : ''}
                  </p>
                </div>
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ChannelDetail;
