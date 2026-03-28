import axios from 'axios'

const apiClient = axios.create({
    baseURL: `${import.meta.env.VITE_API_URL ?? 'http://localhost:8000'}/api/agents`,
    headers: { 'Content-Type': 'application/json' }
});

export function startGame(username) {
    return apiClient.get('/challenge', { params: { username }});
}