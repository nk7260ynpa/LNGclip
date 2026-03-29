import { useNavigate } from 'react-router-dom';

function ChannelDetail() {
  const navigate = useNavigate();

  return (
    <div>
      <button
        className="btn btn-secondary"
        onClick={() => navigate('/')}
        style={{ marginBottom: 16 }}
      >
        返回首頁
      </button>
      <div className="empty-state">頻道詳細頁面（之後規劃）</div>
    </div>
  );
}

export default ChannelDetail;
