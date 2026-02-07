<script setup>
    import { onMounted, ref, onBeforeUnmount } from 'vue';
    import maplibregl from 'maplibre-gl';
    import 'maplibre-gl/dist/maplibre-gl.css';

    const props = defineProps({
        height: {
            type: Number,
            default: 500,
        },
        mapStyle: {
            type: String,
            default: 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
        }
    });

    // Références
    const mapContainer = ref(null);
    const map = ref(null);
    const centerCoords = ref(null);

    const emit = defineEmits(['area-selected']);

    /**
     * Calcule les coordonnées d'un carré autour d'un point central
     */
    const calculateSquareCoords = (center, sizeKm) => {
        const degPerKm = 0.009; // Approximation pour le calcul de zone
        const { lng, lat } = center;
        return [
            [lng - degPerKm * sizeKm, lat - degPerKm * sizeKm],
            [lng + degPerKm * sizeKm, lat - degPerKm * sizeKm],
            [lng + degPerKm * sizeKm, lat + degPerKm * sizeKm],
            [lng - degPerKm * sizeKm, lat + degPerKm * sizeKm],
            [lng - degPerKm * sizeKm, lat - degPerKm * sizeKm]
        ];
    };

    /**
     * Dessine ou met à jour le rectangle sur la carte
     */
    const drawSquare = (center) => {
        const coords = calculateSquareCoords(center, 0.5);
        const sourceName = 'study-area';

        if (map.value.getSource(sourceName)) {
            map.value.getSource(sourceName).setData({
                type: 'Feature',
                geometry: { type: 'Polygon', coordinates: [coords] }
            });
        } else {
            map.value.addSource(sourceName, {
                type: 'geojson',
                data: {
                    type: 'Feature',
                    geometry: { type: 'Polygon', coordinates: [coords] }
                }
            });
            map.value.addLayer({
                id: 'study-area-layer',
                type: 'fill',
                source: sourceName,
                paint: {
                    'fill-color': '#3f51b5',
                    'fill-opacity': 0.3,
                    'fill-outline-color': '#1a237e'
                }
            });
        }
    };

    onMounted(() => {
        map.value = new maplibregl.Map({
            container: mapContainer.value,
            style: props.mapStyle,
            center: [6.8485, 47.6397], // Belfort
            zoom: 13,
        });

        map.value.addControl(new maplibregl.NavigationControl(), 'top-right');

        map.value.on('click', (e) => {
            centerCoords.value = e.lngLat;
            
            drawSquare(e.lngLat);
            
            emit('area-selected', {
                center: e.lngLat,
                square: calculateSquareCoords(e.lngLat, 0.5)
            });
        });
    });

    onBeforeUnmount(() => {
        if (map.value) {
            map.value.remove();
        }
    });
</script>

<template>
    <div
        ref="mapContainer"
        class="street-map"
        :style="{
            '--street-map__height': `${height}px`,
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