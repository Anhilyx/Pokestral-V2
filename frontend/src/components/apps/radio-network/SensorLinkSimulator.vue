<script setup>
    import { ref, computed } from 'vue';

    /**************
    | Form Inputs |
    **************/
    const power = ref(20);
    const frequency = ref(2600);
    const distance = ref(0.1);
    const antennaHeight = ref(30);
    const isUrban = ref(true);  // Multiplier for environment

    /****************
    | Static Values |
    ****************/
    const NOISE_INTERFERENCE = -100;
    const SENSITIVITY_THRESHOLD = -90;
    const BEST_SIGNAL = -50;

    /******************
    | Computed Values |
    ******************/

    // Compute environment-based values
    const sensorHeight = computed(() => 1.5);
    const antennaHeightCorrection = computed(() => {
        if (isUrban.value) return (
            3.2 * Math.pow(
                Math.log10(11.75 * sensorHeight.value), 2)
            - 4.97
        );
       
        else return (
            (1.1 * Math.log10(frequency.value) - 0.7) * sensorHeight.value
            - (1.56 * Math.log10(frequency.value) - 0.8)
        );
    });
    const powerCorrection = computed(() => {
        return isUrban.value ? 3 : 0;
    });
    // Compute path loss using Cost-Hata Model
    const pathLoss = computed(() => {
        // Base value
        let value = (
            46.3
            + 33.9 * Math.log10(frequency.value)
            - 13.82 * Math.log10(antennaHeight.value)
            - antennaHeightCorrection.value
            + (44.9 - 6.55 * Math.log10(antennaHeight.value)) * Math.log10(distance.value)
            + powerCorrection.value
        );

        // Suburban correction
        if (!isUrban.value) value -= (
            2 * Math.pow(Math.log10(frequency.value / 28), 2)
            + 5.4
        );

        return value;
    });

    // Adjust values due to path loss
    const rcvPower = computed(() => {
        if (distance.value <= 0) return power.value;
        return power.value - pathLoss.value;
    });
</script>

<template>
    <HoloApp
        title="Sensor Link Simulator"
        :status="{
            output:
                (rcvPower < NOISE_INTERFERENCE) ? 'error'
                : (rcvPower < SENSITIVITY_THRESHOLD) ? 'warning'
                : undefined
        }"
        :outputs="2"
    >

        <template #input>
            <!-- Sensor Power Selection -->
            <HoloSelect
                label="Sensor Power (dBm)"

                v-model="power"
                :items="[
                    { title: '20 dBm (Standard)',   value: 20},
                    { title: '23 dBm (High Power)', value: 23},
                ]"
            />

            <!-- Frequency Input -->
            <HoloTextField
                label="Frequency (MHz)"
                placeholder="Ex: 2600 or 800"
                type="number"

                v-model="frequency"
                :min="2550"
                :max="2650"
                :step="5"
            />

            <!-- Distance Slider -->
            <HoloSlider
                label="Distance (km)"
                :log="true"
                unit="km"

                v-model="distance"
                :min="0.01"
                :max="10"
            />

            <!-- Antenna Height Slider -->
            <HoloSlider
                label="Antenna Height (m)"
                unit="m"

                v-model="antennaHeight"
                :min="10"
                :max="40"
                step="1"
            />

            <!-- Cyclic Prefix Mode Selection -->
            <HoloSelect
                label="Environment"

                v-model="isUrban"
                :items="[
                    { title: 'Dense Urban', value: true },
                    { title: 'Suburban',    value: false },
                ]"
            />
        </template>

        <template #output-1>
            <div style="height: 20px;"></div>

            <!-- Bars version -->
            <VContainer>
                <VRow>
                    <VCol cols="6" class="pa-0 pr-3">
                        <NetworkBars
                            :value="
                                rcvPower >=  -60 ? 5 :
                                rcvPower >=  -70 ? 4 :
                                rcvPower >=  -80 ? 3 :
                                rcvPower >=  -90 ? 2 :
                                rcvPower >= -100 ? 1 :
                                0"
                            :max="5"
                        />
                    </VCol>

                    <VCol cols="6" class="pa-0 d-flex flex-column justify-center">
                        <div class="sinr">
                            <span class="strong"> {{ (rcvPower).toFixed(1) }} </span>
                            <span class="weak"> dBm </span>
                        </div>
                        <div class="modulation">
                            <span class="strong">{{
                                rcvPower >= -60 ? 'Excellent' :
                                rcvPower >= -70 ? 'Very Good' :
                                rcvPower >= -80 ? 'Good' :
                                rcvPower >= -90 ? 'Fair' :
                                rcvPower >=-100 ? 'Poor' :
                                'No Signal'

                            }}</span>
                        </div>
                    </VCol>
                </VRow>
            </VContainer>

            <div style="min-height: 20px; flex-grow: 1;"></div>

            <!-- Data -->
            <DataList
                class="pa-0"
                :items="[
                    {
                        title: 'Received Power',
                        value: `${rcvPower.toFixed(2)} dBm`
                    },
                    {
                        title: 'Path Loss',
                        value: `${pathLoss.toFixed(2)} dB`
                    }
                ]"
            />

        </template>

        <template #output-2>

            <!-- Gauge version -->
            <div class="d-flex justify-center">
                <Gauge
                    :percent="(
                        Math.max(Math.min(
                            ((rcvPower - NOISE_INTERFERENCE)
                            / (BEST_SIGNAL - NOISE_INTERFERENCE))
                            * 100
                        , 100), 0)
                    )"
                    :value="`${(rcvPower - NOISE_INTERFERENCE).toFixed(1)} dBm`"
                />
            </div>

            <div style="min-height: 20px; flex-grow: 1;"></div>

            <!-- Data -->
            <DataList
                class="pa-0"
                :items="[
                    {
                        title: 'Received Power',
                        value: `${rcvPower.toFixed(2)} dBm`
                    },
                    {
                        title: 'Above Noise',
                        value: `${(rcvPower - NOISE_INTERFERENCE).toFixed(2)} dB`
                    }
                ]"
            />

        </template>
    </HoloApp>
</template>

<style scoped>
    .spacer {
        min-height: 40px;
        flex-grow: 1;
    }

    .network-bars {
        /* Size */
        height: 80px;
    }

    .gauge {
        /* Size */
        height: 100px;
        width: 75%;
    }
</style>