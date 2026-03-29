import { useState, useEffect, useCallback } from 'react';
import { getVideos, triggerCrawl } from '../services/api';

function Home() {
  const [videos, setVideos] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [searchInput, setSearchInput] = useState('');
  const [search, setSearch] = useState('');
  const [crawling, setCrawling] = useState(false);

  const loadVideos = useCallback(() => {
    setLoading(true);
    getVideos(page, 9, search || undefined)
      .then((data) => {
        setVideos(data.videos);
        setTotalPages(data.total_pages);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [page, search]);

  useEffect(() => {
    loadVideos();
  }, [loadVideos]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    setSearch(searchInput);
  };

  const handleCrawl = async () => {
    setCrawling(true);
    try {
      const result = await triggerCrawl();
      alert(
        `檢查完成：${result.channels_processed} 個頻道，新增 ${result.total_new_videos} 部影片（耗時 ${result.elapsed_seconds} 秒）`
      );
      setPage(1);
      loadVideos();
    } catch (err) {
      alert(`檢查失敗：${err.message}`);
    } finally {
      setCrawling(false);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>LNG 精華影片</h2>
        <button
          className="btn btn-primary"
          onClick={handleCrawl}
          disabled={crawling}
        >
          {crawling ? '檢查中...' : '檢查新影片'}
        </button>
      </div>
      <form className="search-bar" onSubmit={handleSearch}>
        <input
          type="text"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          placeholder="搜尋影片標題..."
        />
        <button type="submit" className="btn btn-primary">搜尋</button>
      </form>

      {loading ? (
        <div className="empty-state">載入中...</div>
      ) : videos.length === 0 ? (
        <div className="empty-state">
          {search ? '找不到符合的影片' : '尚無影片'}
        </div>
      ) : (
        <>
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
        </>
      )}
    </div>
  );
}

export default Home;
