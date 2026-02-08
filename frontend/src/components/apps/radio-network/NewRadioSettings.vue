<script setup>
    import HoloStreetMapPlus from '@/components/apps/radio-network/components/HoloStreetMapPlus.vue';
    import { getBuildings } from '@/services/radio-network';

    async function onAreaChanged(data) {
        console.log(await getMeanHeight(data.coordinates));
    }

    /**
     * Fetch building heights for the given coordinates and handle pagination if necessary.
     * @param coordinates - The coordinates defining the area for which to fetch building heights.
     */
    async function getMeanHeight(coordinates) {
        const timestamp = Date.now();

        // 1. Fetch all the buildings for the given area
        const buildings = [];
        try {
            // Initial fetch for the first page of building data
            let response = await getBuildings(coordinates).then(res => res.data);
            buildings.push(...response.features);

            // Compute number of pages (in the case where the total features are less than the requested number of features, it will always return 1 page)
            const pages = Math.ceil(response.totalFeatures / response.features.length);

            // Fetch remaining pages
            for (let page = 1; page < pages; page++) {
                response = await getBuildings(coordinates, page).then(res => res.data);
                buildings.push(...response.features);
            }
        } catch (error) {
            // Handle any errors that occur while fetching building heights
            console.error('Error fetching building heights:', error);
        }

        // 2. Extract and return the average height for all the buildings
        let totalHeight = 0;
        let count = 0;
        buildings.forEach(building => {
            // Extract data
            const properties = building.properties;
            const minGroundHeight = properties.altitude_minimale_sol;
            const maxGroundHeight = properties.altitude_maximale_sol;
            const minRoofHeight = properties.altitude_minimale_toit;
            const maxRoofHeight = properties.altitude_maximale_toit;

            const groundHeight = minGroundHeight ??
                                 maxGroundHeight ??
                                 null;
            const roofHeight = maxRoofHeight ??
                               minRoofHeight ??
                               null;

            // Check values
            if (groundHeight === null || roofHeight === null)
                return;

            // Update total height and count
            totalHeight += (roofHeight - groundHeight);
            count++;
        });

        // Log the time taken to fetch and process building heights
        console.log(`Fetched building heights in ${Date.now() - timestamp} ms`);
        return totalHeight / count;
    }
</script>

<template>
    <HoloApp
        title="5G Settings"
        :status="{
            output: true,
        }"
        :outputs="2"
    >

        <template #input>
            <HoloStreetMapPlus
                @area-changed="onAreaChanged"
            />
        </template>

        <template #output-1>
        </template>

        <template #output-2>
        </template>
    </HoloApp>
</template>

<style scoped>
</style>