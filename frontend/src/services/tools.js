import axios from 'axios'

const apiClient = axios.create({
    baseURL: `${import.meta.env.API_URL ?? 'http://localhost:3001'}/api/tools`,
    headers: { 'Content-Type': 'application/json' }
});

export function calculateDamage_knownAttacker(data) {
    return apiClient.post('/damage-calculator/known-attacker', data);
}
export function calculateDamage_knownDefender(data) {
    return apiClient.post('/damage-calculator/known-defender', data);
}
export function calculateDamage_knownBoth(data) {
    return apiClient.post('/damage-calculator/known-both', data);
}
export function calculateDamage_knownNone(data) {
    return apiClient.post('/damage-calculator/known-none', data);
}