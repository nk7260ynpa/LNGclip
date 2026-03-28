import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import ChannelDetail from './pages/ChannelDetail';
import Admin from './pages/Admin';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="App-nav">
          <Link to="/" className="nav-brand">LNGclip</Link>
          <div className="nav-links">
            <Link to="/">首頁</Link>
            <Link to="/admin">管理</Link>
          </div>
        </nav>
        <main className="App-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/channel/:id" element={<ChannelDetail />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
