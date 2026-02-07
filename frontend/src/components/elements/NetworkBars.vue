<script setup>
    import { computed } from 'vue';

    const props = defineProps({
        value: {
            type: Number,
            required: true
        },
        max: {
            type: Number,
            default: 5
        },

        color: {
            type: String,
            default: null
        }
    });

    const computedColor = computed(() => {
        // Use custom color if provided
        if (props.color)
            return props.color;
       
        // Else use hst-based color scaling
        const progress = (props.value - 1) / (props.max - 1);  // Between 1 and max
        const hue = progress * 120;  // Between 0 (red) and 120 (green)

        return `hsl(${hue}, 100%, 50%)`;
    });
</script>

<template>
    <div class="network-bars">
        <div v-for="i in props.max"
            :key="`bar-${i}`"
            class="network-bars__wrapper"
        >
            <div class="network-bars__bar"
                :class="{ active: i <= props.value }"
                :style="{
                    '--color': computedColor,
                    'height': `${20 + (i / props.max) * 80}%`,
                }"
            ></div>
        </div>
    </div>
</template>

<style scoped>
    /* Variables */
    .network-bars {
        /* Size */
        --network-bars__bar-width-percent: 80%;

        /* Style */
        --network-bars__bar-smoothness: 4px;

        /* Glow effect */
        --network-bars__glow-spread: 8px;
    }

    .network-bars {
        /* Layout */
        display: flex;
        padding: var(--network-bars__glow-spread);
    }

    .network-bars__wrapper {
        /* Layout */
        display: flex;
        align-items: flex-end;
        justify-content: center;

        /* Size */
        flex-grow: 1;
    }

    .network-bars__bar {
        /* Shape */
        width: var(--network-bars__bar-width-percent);
        border-radius: var(--network-bars__bar-smoothness);

        /* Default color */
        background-color: var(--container-background-empty);
        box-shadow: none;

        /* Animation */
        transition: background-color var(--animation-speed-medium),
                    box-shadow var(--animation-speed-medium);
    }

    .network-bars__bar.active {
        background-color: var(--color);
        box-shadow: 0 0 var(--network-bars__glow-spread) var(--color);
    }
</style>