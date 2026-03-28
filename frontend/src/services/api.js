const API_BASE = process.env.REACT_APP_API_URL || '/api';

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

// 頻道 API
export function getChannels(activeOnly = false) {
  const query = activeOnly ? '?active_only=true' : '';
  return request(`/channels${query}`);
}

export function getChannel(id) {
  return request(`/channels/${id}`);
}

export function createChannel(data) {
  return request('/channels', { method: 'POST', body: JSON.stringify(data) });
}

export function updateChannel(id, data) {
  return request(`/channels/${id}`, { method: 'PUT', body: JSON.stringify(data) });
}

export function deleteChannel(id) {
  return request(`/channels/${id}`, { method: 'DELETE' });
}

export function toggleChannel(id) {
  return request(`/channels/${id}/toggle`, { method: 'PATCH' });
}

// 影片 API
export function getChannelVideos(channelId) {
  return request(`/channels/${channelId}/videos`);
}

// 同步 API
export function syncChannel(id) {
  return request(`/channels/${id}/sync`, { method: 'POST' });
}

export function syncAll() {
  return request('/sync', { method: 'POST' });
}
