import { useState, useEffect } from 'react';
import { getVideos } from '../services/api';

function Home() {
  const [videos, setVideos] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getVideos(page, 6)
      .then((data) => {
        setVideos(data.videos);
        setTotalPages(data.total_pages);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [page]);

  if (loading) return <div className="empty-state">載入中...</div>;

  if (videos.length === 0) {
    return <div className="empty-state">尚無影片</div>;
  }

  return (
    <div>
      <h2>LNG 精華影片</h2>
      <div className="embed-grid">
        {videos.map((v) => (
          <a
            key={v.video_id}
            className="thumb-card"
            href={`https://www.youtube.com/watch?v=${v.video_id}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            <div className="thumb-wrapper">
              <img
                src={v.thumbnail || `https://i.ytimg.com/vi/${v.video_id}/mqdefault.jpg`}
                alt={v.title}
              />
            </div>
            <div className="thumb-title">{v.title}</div>
          </a>
        ))}
      </div>
      <div className="pagination">
        <button
          className="btn btn-secondary"
          disabled={page <= 1}
          onClick={() => setPage(page - 1)}
        >
          上一頁
        </button>
        <span className="page-info">{page} / {totalPages}</span>
        <button
          className="btn btn-secondary"
          disabled={page >= totalPages}
          onClick={() => setPage(page + 1)}
        >
          下一頁
        </button>
      </div>
    </div>
  );
}

export default Home;
