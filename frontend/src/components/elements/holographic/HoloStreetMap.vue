<script setup>
    import { ref } from 'vue';

    const mapRef = ref(null);

    defineExpose({
        mapRef
    });

    defineOptions({
        inheritAttrs: false
    });
</script>

<template>
    <HoloTheme class="holo-street-map">
        <div class="holo-street-map__border">
            <div class="holo-street-map__color">
                <StreetMap
                    v-bind="$attrs"
                    @load="$emit('load', $event)"
                    ref="mapRef"
                    map-style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
                />
            </div>
        </div>
    </HoloTheme>
</template>

<style scoped>
    /* Variables */
    .holo-street-map {
        /* Border */
        --holo-street-map__roundness: 12px;
        --holo-street-map__border-width: 20px;
        --holo-street-map__border-glow-weak-base:     calc(var(--holo-street-map__border-width) / 2 * 1.0);
        --holo-street-map__border-glow-weak-spread:   calc(var(--holo-street-map__border-width) / 2 * 0.2);
        --holo-street-map__border-glow-strong-base:   calc(var(--holo-street-map__border-width) / 2 * 0.5);
        --holo-street-map__border-glow-strong-spread: calc(var(--holo-street-map__border-width) / 2 * 0.1);
        --holo-street-map__border-glow-weak: var(--holo-street-map__border-glow-weak-base) var(--holo-street-map__border-glow-weak-spread);
        --holo-street-map__border-glow-strong: var(--holo-street-map__border-glow-strong-base) var(--holo-street-map__border-glow-strong-spread);

        /* Controls */
        --holo-street-map__ctrl-glow-strength: 0 0 4px 2px;
        --holo-street-map__ctrl-glow-color: var(--holo-theme__glow-bright-strong);
    }

    /***** Borders *****/

    .holo-street-map__border {
        /* Layout */
        position: relative;
        margin: calc(var(--holo-street-map__border-width) / 2) calc(var(--holo-street-map__border-width) / 2);
    }

    :deep(.street-map) {
        border-radius: var(--holo-street-map__roundness);
    }

    .holo-street-map__color {
        border-radius: var(--holo-street-map__roundness);
    }

    .holo-street-map__border::after {
        content: "";

        /* Position */
        position: absolute;
        inset: 0;
        z-index: 10;
       
        /* Borders */
        border-radius: var(--holo-street-map__roundness);
        box-shadow:       0 0 var(--holo-street-map__border-glow-weak)   var(--holo-theme__glow-bright-weak),
                          0 0 var(--holo-street-map__border-glow-strong) var(--holo-theme__glow-bright-strong),
                    inset 0 0 var(--holo-street-map__border-glow-weak)   var(--holo-theme__glow-bright-weak),
                    inset 0 0 var(--holo-street-map__border-glow-strong) var(--holo-theme__glow-bright-strong);

        /* Prevent interaction */
        pointer-events: none;
    }

    /***** Recolor *****/

    .holo-street-map__color {
        position: relative;
    }

    :deep(.maplibregl-canvas) {
        /* Convert map to grayscale */
        filter: grayscale(1) brightness(2);
    }

    .street-map::after {
        content: "";

        /* Position */
        position: absolute;
        inset: 0;
        z-index: 1;

        /* Color overlay */
        border-radius: var(--holo-street-map__roundness);
        background: var(--holo-theme__background-color);
        mix-blend-mode: multiply;

        /* Prevent interaction */
        pointer-events: none;
    }

    :deep(.maplibregl-ctrl) {
        background-color: var(--holo-street-map__ctrl-glow-color) !important;
        box-shadow: var(--holo-street-map__ctrl-glow-strength) var(--holo-street-map__ctrl-glow-color) !important;
        mix-blend-mode: multiply;
    }
</style>