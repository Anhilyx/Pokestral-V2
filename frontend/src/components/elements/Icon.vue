<script setup>
    const props = defineProps({
        icon: {
            type: String,
            required: true
        },

        fill: {
            type: Boolean,
            default: false
        },
        weight: {
            type: Number,
            default: 300,
            min: 100,
            max: 700
        },
        grade: {
            type: Number,
            default: 0,
            min: -25,
            max: 200
        },
        opticalSize: {
            type: Number,
            default: null,
            min: 20,
            max: 48
        },

        size: {
            type: Number,
            default: 24
        }
    });
</script>

<template>
    <span class="icon material-symbols-outlined no-select" :style="{
        'font-variation-settings':
            `'FILL' ${fill ? 1 : 0}, ` +
            `'wght' ${weight}, ` +
            `'GRAD' ${grade}, ` +
            `'opsz' ${opticalSize ?? Math.min(Math.max(size, 20), 48)}`,
        'font-size': `${size}px`
    }">
        {{ icon }}
    </span>
</template>