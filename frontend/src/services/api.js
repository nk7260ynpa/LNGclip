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

export function getChannels() {
  return request('/channels');
}

export function createChannel(data) {
  return request('/channels', { method: 'POST', body: JSON.stringify(data) });
}

export function deleteChannel(id) {
  return request(`/channels/${id}`, { method: 'DELETE' });
}

export function fetchMetadata(id) {
  return request(`/channels/${id}/fetch-metadata`, { method: 'POST' });
}

export function backfillChannels() {
  return request('/channels/backfill', { method: 'POST' });
}

export function getVideos(page = 1, perPage = 9, search) {
  let url = `/videos?page=${page}&per_page=${perPage}`;
  if (search) url += `&search=${encodeURIComponent(search)}`;
  return request(url);
}
