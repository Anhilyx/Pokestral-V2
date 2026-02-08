<script setup>
    import { ref } from 'vue';
    import { getBuildings, getRoads, getPopulation } from '@/services/radio-network';
    import HoloStreetMapPlus from '@/components/apps/radio-network/components/HoloStreetMapPlus.vue';

    // Values used to display the results
    const areaWidth = ref(null);
    const areaHeight = ref(null);
    const averageHeight = ref(null);
    const buildingsCount = ref(null);
    const averageSpeed = ref(null);
    const averageHighSpeed = ref(null);
    const roadsCount = ref(null);
    const averageDensity = ref(null);
    const cities = ref([]);
    const recommandedSCS = ref(null);
    const recommandedBandwidth = ref(null);
    const recommandedMode = ref(null);

    // Used to only keep the latest requests
    const currentId = ref(0);
    const maxId = ref(-2);
    const error = ref(false);

    async function onAreaChanged(data) {
        let id = currentId.value++;

        const avgHeightData = await getMeanHeight(data.coordinates);
        const avgSpeedData = await getMeanTraffic(data.coordinates);
        const avgPopulationData = await getPopDensity(data.coordinates);

        // Check if results are corrects
        if (!avgHeightData || !avgSpeedData || !avgPopulationData) {
            if (id > maxId.value) {
                console.error('Error fetching data for the selected area');
                maxId.value = id;
                error.value = true;
            }
            return;
        }

        // Compute area width and height in km
        const latDiff = Math.abs(data.coordinates.minLat - data.coordinates.maxLat);
        const lngDiff = Math.abs(data.coordinates.minLng - data.coordinates.maxLng);
        const width = lngDiff * 111.32 * Math.cos((data.coordinates.minLat + data.coordinates.maxLat) / 2 * Math.PI / 180); // in km
        const height = latDiff * 110.574; // in km

        // Compute required parameters for the 5G network based on the fetched data and area size
        let                              scs =  '15 kHz';
        if (avgSpeedData.average >   50) scs =  '30 kHz';
        if (avgSpeedData.average >=  80) scs =  '60 kHz';
        if (avgSpeedData.top10   >  110) scs = '120 kHz';

        let                                   bandwidth = '3.5 GHz';
        if (avgPopulationData.average <  300) bandwidth = '700 MHz';  // Official data for 'low density'
        if (avgPopulationData.average > 1500
         && avgHeightData.average < 15)       bandwidth = '24 GHz'; // Official data for 'urban center' + low building heights

        let                             mode = 'Normal'
        if (width * height > 1) mode = 'Extended';  // If the area is bigger than 1 km², we switch to extended mode to increase the coverage radius of each antenna

        // Update the displayed values
        if (id > maxId.value) {
            maxId.value = id;
            
            areaWidth.value = width.toFixed(2);
            areaHeight.value = height.toFixed(2);
            averageHeight.value = avgHeightData.average.toFixed(2);
            buildingsCount.value = avgHeightData.count;
            averageSpeed.value = avgSpeedData.average.toFixed(2);
            averageHighSpeed.value = avgSpeedData.top10.toFixed(2);
            roadsCount.value = avgSpeedData.count;
            averageDensity.value = avgPopulationData.average.toFixed(2);
            cities.value = avgPopulationData.cities;
            recommandedSCS.value = scs;
            recommandedBandwidth.value = bandwidth;
            recommandedMode.value = mode;
        }
    }

    /**
     * Fetch building heights for the given coordinates and handle pagination if necessary.
     * @param coordinates - The coordinates defining the area for which to fetch building heights.
     */
    async function getMeanHeight(coordinates) {
        const timestamp1 = Date.now();

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
            return null;
        }

        const timestamp2 = Date.now();

        // 2. Extract the average height for all the buildings
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
        const averageHeight = totalHeight / count;

        // Log the time taken to fetch and process building heights
        const timestamp3 = Date.now();
        console.log(`Fetched building heights in ${timestamp3 - timestamp1} ms (${timestamp2 - timestamp1}ms | ${timestamp3 - timestamp2}ms)`);

        // Return results
        error.value = false;
        return {
            average: averageHeight,
            count,
            duration: timestamp3 - timestamp1
        };
    }
    
    /**
     * Fetch road traffic for the given coordinates and handle pagination if necessary.
     * @param coordinates - The coordinates defining the area for which to fetch road traffic.
     */
    async function getMeanTraffic(coordinates) {
        const timestamp1 = Date.now();

        // 1. Fetch all the roads for the given area
        const roads = [];
        try {
            // Overpass seems to return all the roads in one go
            let response = await getRoads(coordinates).then(res => res.data);
            roads.push(...response.elements);

        } catch (error) {
            // Handle any errors that occur while fetching building heights
            console.error('Error fetching road speeds:', error);
            return null;
        }

        const timestamp2 = Date.now();

        // 2. Extract the average speed for all the roads
        let totalSpeed = 0;
        let count = 0;
        roads.forEach(road => {
            // Extract data
            const maxspeed = parseInt(road.tags?.maxspeed);

            // Check values
            if (isNaN(maxspeed))
                return;

            // Update total height and count
            totalSpeed += maxspeed;
            count++;
        });
        const averageSpeed = totalSpeed / count;

        const timestamp3 = Date.now();

        // 3. Extract the top 10% fastest roads and return their average speed
        const sortedRoads = roads
            .filter(road => !isNaN(parseInt(road.tags?.maxspeed)))
            .sort((a, b) => parseInt(b.tags.maxspeed) - parseInt(a.tags.maxspeed));
        const topSpeed = sortedRoads
                         .slice(0, Math.ceil(count * 0.1))
                         .reduce((sum, road) => sum + parseInt(road.tags.maxspeed), 0)
                         / Math.ceil(count * 0.1);

        // Log the time taken to fetch and process building heights
        const timestamp4 = Date.now();
        console.log(`Fetched road speeds in ${timestamp4 - timestamp1} ms (${timestamp2 - timestamp1}ms | ${timestamp4 - timestamp2}ms)`);

        // Return results
        return {
            average: averageSpeed,
            top10: topSpeed,
            count,
            duration: timestamp4 - timestamp1
        };
    }

    /**
     * Fetch population density for the given coordinates and handle pagination if necessary.
     * @param coordinates - The coordinates defining the area for which to fetch population density.
     */
    async function getPopDensity(coordinates) {
        const timestamp1 = Date.now();

        // 1. Fetch the population for the given area
        const cities = [];
        try {
            // We assume that the population endpoint returns all the cities in one go (in fact, we assume that only one city is returned, but we handle the case where multiple cities are returned just in case)
            let response = await getPopulation(coordinates).then(res => res.data);
            cities.push(...response);

        } catch (error) {
            // Handle any errors that occur while fetching building heights
            console.error('Error fetching population:', error);
            return null;
        }

        const timestamp2 = Date.now();

        // 2. Extract the average population density of all the cities
        let totalDensity = 0;
        let count = 0;
        cities.forEach(city => {
            // Extract data
            const rawArea = city.surface;  // in hectares
            const population = city.population;

            // Check values
            if (isNaN(rawArea) || isNaN(population))
                return;

            // Convert area from ha to km²
            const area = rawArea / 100; // 1 km² = 100 ha
            // Convert population to density (people per km²)
            const density = population / area;

            // Update total density and count
            totalDensity += density;
            count++;
        });
        const averageDensity = totalDensity / count;

        // Log the time taken to fetch and process building heights
        const timestamp3 = Date.now();
        console.log(`Fetched population density in ${timestamp3 - timestamp1} ms (${timestamp2 - timestamp1}ms | ${timestamp3 - timestamp2}ms)`);

        // Return results
        return {
            average: averageDensity,
            count,
            cities: cities
                    .sort((a, b) => b.population - a.population)  // Sort cities by population
                    .map(city => city.nom),
            duration: timestamp3 - timestamp1
        };
    }
</script>

<template>
    <HoloApp
        title="5G Settings"
        :status="{
            'output': error ? 'error' : ''
        }"
        :outputs="2"
        :width="900"
    >

        <template #input>
            <HoloStreetMapPlus
                @area-changed="onAreaChanged"
            />
        </template>

        <template #output-1>
            <!-- Show loading if no result -->
            <div
                v-if="maxId < currentId - 1 || error"
                class="d-flex justify-center align-center flex-grow-1"
            >
                <!-- Progress differs between with and without error -->
                <VProgressCircular
                    :class="{
                        'glitch': error ?? false
                    }"
                    color="var(--holo-theme__background-color)"
                    size="64" width="6"
                    indeterminate
                />
            </div>

            <div v-else>
                <h3> Area information </h3>
                <DataList
                    :items="[
                        { title: 'Area size',                  value: `${areaWidth}x${areaHeight} km` },
                        { title: 'Average building height',    value: `${averageHeight} m`            },
                        { title: 'Average road speed',         value: `${averageSpeed} km/h`          },
                        { title: '10% fastest roads',          value: `${averageHighSpeed} km/h`      },
                        { title: 'Average population density', value: `${averageDensity} ppl/km²`     },
                    ]"
                />

                <h3> Statistics </h3>
                <DataList
                    :items="[
                        { title: 'Buildings found',     value: `${buildingsCount}`     },
                        { title: 'Road sections found', value: `${roadsCount}`         },
                        { title: 'Cities found',        value: `${cities.length}`      },
                        { title: 'Most populated city', value: `${cities[0] ?? 'N/A'}` }
                    ]"
                />
            </div>
        </template>

        <template #output-2>
            <!-- Show loading if no result -->
            <div
                v-if="maxId < currentId - 1"
                class="d-flex justify-center align-center flex-grow-1"
            >
                <!-- Progress differs between with and without error -->
                <VProgressCircular
                    :class="{
                        'glitch': error ?? false
                    }"
                    color="var(--holo-theme__background-color)"
                    size="64" width="6"
                    indeterminate
                />
            </div>

            <div v-else-if="error">
                <h3> Error fetching data </h3>
                <p>
                    An error occurred while fetching data for the selected area. This can be due to several reasons:
                </p>
                <ul>
                    <li> The selected area is too big and contains too many buildings/roads/cities, which causes the API to fail. Try selecting a smaller area. </li>
                    <li> The selected area is in a region where data is not available (e.g. outside of France). Try selecting an area in France. </li>
                    <li> There is a temporary issue with the API. Try again later. </li>
                </ul>
            </div>

            <div v-else>
                <h3> Recommanded values </h3>
                <DataList
                    :items="[
                        { title: 'Subcarriers Spacing', value: recommandedSCS        },
                        { title: 'Bandwidth',           value: recommandedBandwidth  },
                        { title: 'Mode',                value: `${recommandedMode}*` },
                    ]"
                />

                <p class="weak" style="text-align: justify">
                    * The recommanded mode depends on the covered area. However, if you decide to spread multiple antennas over this area, this value can change from <i>Extended</i> to <i>Normal</i>. And if you only select a part of the area covered by a single antenna, it can change from <i>Normal</i> to <i>Extended</i>.
                </p>
            </div>
        </template>
    </HoloApp>
</template>

<style scoped>
</style>