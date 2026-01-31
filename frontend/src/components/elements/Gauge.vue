<script setup>
    import { computed } from 'vue';

    const props = defineProps({
        percent: {
            type: Number,
            required: true
        },
        value: {
            default: undefined
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
        const hue = props.percent / 100 * 150;  // Between 0 (red) and 150 (cyan/green)

        return `hsl(${hue}, 100%, 50%)`;
    });
</script>

<template>
    <div class="gauge">
        <div class="gauge__wrapper">
            <div class="gauge__container"
                :style="{
                    '--angle': `${props.percent / 100 * 190}deg`,
                    '--color': computedColor
                }"
            >
                <!-- Gauge Visual -->
                <div class="gauge__background"></div>
                <div class="gauge__fill"></div>
                <div class="gauge__glow"></div>

                <!-- Gauge Value -->
                <div class="gauge__value"
                    :style="{
                        '--percent': props.percent / 100
                    }"
                >
                    <h2> {{
                        props.value === undefined ?
                        `${props.percent.toFixed(0)} %` :
                        props.value
                    }} </h2>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    /* Variables */
    .gauge {
        /* Size */
        --gauge__thickness: 18px;

        /* Glow */
        --gauge__glow-spread: 10px;

        /* Text glow */
        --gauge__min-text-glow-spread: 1px;
        --gauge__max-text-glow-spread: 5px;
    }

    .gauge {
        /* Layout */
        overflow-y: hidden;
    }

    .gauge__wrapper {
        /* Size */
        height: 200%;
        width: 100%;
        
        /* Layout */
        padding: var(--gauge__glow-spread);
    }

    /* Properties for animations */
    @property --angle {
        syntax: '<angle>';
        initial-value: 0deg;
        inherits: false;
    }
    @property --color {
        syntax: '<color>';
        initial-value: transparent;
        inherits: false;
    }

    .gauge__container {
        /* Layout */
        position: relative;
        width: 100%;
        height: 100%;

        /* Fill/Glow gradient */
        --gradient: conic-gradient(
            from 260deg,
            var(--color) 0deg,
            var(--color) var(--angle),
            transparent calc(var(--angle) + 10deg),
            transparent 360deg
        );
        --text-color: var(--color);

        /* Animation */
        transition: --angle var(--animation-speed-fast),
                    --color var(--animation-speed-fast);
    }

    /* Gauge background */
    .gauge__background {
        /* Position */
        position: absolute;
        inset: 0;
        
        /* Shape */
        border-radius: 50%;
        border: solid var(--gauge__thickness);

        /* Background color */
        border-color: var(--container-background-empty);
    }

    /* Gauge fill */
    .gauge__fill {
        /* Position */
        position: absolute;
        inset: 0;
        
        /* Shape */
        border-radius: 50%;
        padding: var(--gauge__thickness);
        
        /* Fill color */
        background: var(--gradient);
        
        /* Hide center */
        mask:          linear-gradient(#fff 0 0) content-box, 
                       linear-gradient(#fff 0 0);
        -webkit-mask:  linear-gradient(#fff 0 0) content-box, 
                       linear-gradient(#fff 0 0);

        -webkit-mask-composite: xor;
        mask-composite: exclude;
    }

    .gauge__glow {
        /* Position */
        position: absolute;
        inset: 0;

        /* Glow effect */
        filter: blur(calc(var(--gauge__glow-spread) / 2));
    }

    /* Gauge glow */
    .gauge__glow::before {
        content: "";

        /* Position */
        position: absolute;
        inset: 0;
        
        /* Shape */
        border-radius: 50%;
        padding: var(--gauge__thickness);
        
        /* Fill color */
        background: var(--gradient);
        
        /* Hide center */
        mask:          linear-gradient(#fff 0 0) content-box, 
                       linear-gradient(#fff 0 0);
        -webkit-mask:  linear-gradient(#fff 0 0) content-box, 
                       linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
    }

    .gauge__value {
        /* Position */
        position: absolute;
        width: 100%;
        height: 50%;

        /* Layout */
        display: flex;
        align-items: end;
        justify-content: center;
        
        /* Text style */
        color: color-mix(
            in srgb,
            var(--text-color) 40%,
            #ddd 60%
        );
        text-shadow: 0 0 calc(var(--gauge__min-text-glow-spread) + (var(--gauge__max-text-glow-spread) - var(--gauge__min-text-glow-spread)) * var(--percent)) var(--text-color);
    }
</style>