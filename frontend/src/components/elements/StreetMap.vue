<script setup>
    import { onMounted, ref, onBeforeUnmount, shallowRef } from 'vue';
    import maplibregl from 'maplibre-gl';
    import 'maplibre-gl/dist/maplibre-gl.css';

    const props = defineProps({
        height: {
            type: Number,
            default: 500
        },
        mapStyle: {
            type: String,
            default: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'
        }
    });

    // References
    const mapContainer = ref(null);
    const mapRef = shallowRef(null);

    const emit = defineEmits(['load']);

    onMounted(() => {
        // Initialize map
        mapRef.value = new maplibregl.Map({
            container: mapContainer.value,
            style: props.mapStyle,
            center: [6.8040841, 47.4955164],
            zoom: 13,
        });

        // Add navigation controls
        mapRef.value.addControl(new maplibregl.NavigationControl(), 'top-right');

        // Emit load event
        mapRef.value.on('load', () => {
            emit('load', mapRef.value);
        });
    });

    onBeforeUnmount(() => {
        if (mapRef.value)
            mapRef.value.remove();
    });

    // Give access to the map instance to parent components
    defineExpose({
        mapRef
    });
</script>

<template>
    <div
        ref="mapContainer"
        class="street-map"
        :style="{
            '--street-map__height': `${height}px`
        }"
    ></div>
</template>

<style scoped>
    .street-map {
        height: var(--street-map__height);
        display: flex;
        flex-direction: column;
    }
</style>