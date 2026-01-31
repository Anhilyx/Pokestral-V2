import axios from 'axios'

const apiClient = axios.create({
    baseURL: 'https://pokestral.anhilyx.fr/api/tools',
    headers: { 'Content-Type': 'application/json' }
});

export function calculateDamage(data) {
    return apiClient.post('/damage-calculator', data);
}