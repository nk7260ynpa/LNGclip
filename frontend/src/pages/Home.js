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
          <div key={v.video_id} className="embed-card">
            <div className="embed-wrapper">
              <iframe
                src={`https://www.youtube.com/embed/${v.video_id}`}
                title={v.title}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
            <div className="embed-title">{v.title}</div>
          </div>
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
