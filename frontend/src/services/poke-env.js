import axios from 'axios'

const apiClient = axios.create({
    baseURL: `${import.meta.env.VITE_API_URL ?? 'http://localhost:8000'}/api/poke-env`,
    headers: { 'Content-Type': 'application/json' }
});

export function createWaiter(data) {
    return apiClient.post('/create/waiter', data);
}
export function createFighter(data) {
    return apiClient.post('/create/fighter', data);
}

export function getTurn(uuid) {
    return apiClient.get('/look/turn', { params: { uuid } });
}
export function getTerrain(uuid) {
    return apiClient.get('/look/terrain', { params: { uuid } });
}
export function getActivePokemons(uuid) {
    return apiClient.get('/look/active-pokemons', { params: { uuid } });
}
export function getTeams(uuid) {
    return apiClient.get('/look/teams', { params: { uuid } });
}
export function getAvailableMoves(uuid) {
    return apiClient.get('/look/available-moves', { params: { uuid } });
}
export function getAvailableSwitches(uuid) {
    return apiClient.get('/look/available-switches', { params: { uuid } });
}

export function sendAction(uuid, data) {
    return apiClient.post('/act/', data, { params: { uuid } });
}