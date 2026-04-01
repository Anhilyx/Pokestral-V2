import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'challenge',
        component: () => import('@/views/MainView.vue')
    },
    {
        path: '/tools',
        name: 'tools',
        component: () => import('@/views/ToolsView.vue')
    },
    {
        path: '/poke-env',
        name: 'poke-env',
        component: () => import('@/views/PokeEnvView.vue')
    },

    // Out of context, but it was funny to keep it
    {
        path: '/radio-network',
        name: 'radio-network',
        component: () => import('@/views/RadioNetworkView.vue')
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router