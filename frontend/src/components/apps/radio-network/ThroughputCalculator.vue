<script setup>
    import { ref, computed } from 'vue';

    /**************
    | Form Inputs |
    **************/
    const bandwidth = ref(10);
    const frequency = ref(2600);
    const distance = ref(1.0);
    const power = ref(20);
    const mode = ref(1);  // Multiplier for cyclic prefix mode

    /****************
    | Static Values |
    ****************/
    const NOISE_INTERFERENCE = -100;
    const SENSITIVITY_THRESHOLD = -90;
    const SINR_TABLE = [
        { snr:  0.0, eff: 0.67, mod: "QPSK",   code: "1/3" },
        { snr:  1.5, eff: 1.00, mod: "QPSK",   code: "1/2" },
        { snr:  4.0, eff: 1.30, mod: "QPSK",   code: "2/3" },
        { snr:  5.0, eff: 1.50, mod: "QPSK",   code: "3/4" },
        { snr:  5.5, eff: 1.60, mod: "QPSK",   code: "4/5" },
        { snr:  7.0, eff: 2.00, mod: "16QAM",  code: "1/2" },
        { snr: 10.0, eff: 2.67, mod: "16QAM",  code: "2/3" },
        { snr: 11.5, eff: 3.00, mod: "16QAM",  code: "3/4" },
        { snr: 13.0, eff: 3.20, mod: "16QAM",  code: "4/5" },
        { snr: 15.0, eff: 4.00, mod: "64QAM",  code: "2/3" },
        { snr: 17.0, eff: 4.50, mod: "64QAM",  code: "3/4" },
        { snr: 18.5, eff: 4.80, mod: "64QAM",  code: "4/5" },
        { snr: 20.0, eff: 5.33, mod: "256QAM", code: "2/3" },
        { snr: 22.0, eff: 6.00, mod: "256QAM", code: "3/4" },
        { snr: 24.0, eff: 6.40, mod: "256QAM", code: "4/5" },
        { snr: 27.0, eff: 7.00, mod: "256QAM", code: "7/8" }
    ];

    /******************
    | Computed Values |
    ******************/

    // Adjust values due to path loss
    const pathLoss = computed(() => {
        if (distance.value <= 0) return 0;
        return 20 * Math.log10(distance.value) + 20 * Math.log10(frequency.value) + 32.45;
    });
    const rcvPower = computed(() => {
        if (distance.value <= 0) return power.value;
        return power.value - pathLoss.value;
    });

    // Determine efficiency
    const sinr = computed(() => {
        // Compute SINR
        const value = rcvPower.value - NOISE_INTERFERENCE;

        // Default SINR table entry
        let data = null;
        // Retrieve current SINR table entry
        for (let i = SINR_TABLE.length - 1; i >= 0; i--) {
            if (value >= SINR_TABLE[i].snr) {
                data = SINR_TABLE[i];
                break;
            }
        }

        return data;
    });

    // Compute throughput
    const throughput = computed(() => {
        if (!sinr.value) return 0;
        if (rcvPower.value < SENSITIVITY_THRESHOLD) return 0;
        return bandwidth.value * sinr.value.eff * mode.value;
    });
    const maxThroughput = computed(() => {
        return bandwidth.value * 8;
    });
</script>

<template>
    <HoloApp
        title="LTE Throughput Calculator"
        :status="{
            output:
                (!sinr) ? 'error'
                : (rcvPower < SENSITIVITY_THRESHOLD) ? 'warning'
                : undefined
        }"
        :outputs="2"
    >

        <template #input>
            <!-- Bandwidth Selection -->
            <HoloSelect
                label="Bandwidth"

                v-model="bandwidth"
                :items="[
                    { title: '1.4 MHz', value:  1.4 },
                    { title:   '3 MHz', value:  3   },
                    { title:   '5 MHz', value:  5   },
                    { title:  '10 MHz', value: 10   },
                    { title:  '15 MHz', value: 15   },
                    { title:  '20 MHz', value: 20   },
                ]"
            />

            <!-- Frequency Input -->
            <HoloTextField
                label="Frequency (MHz)"
                placeholder="Ex: 2600 or 800"
                type="number"

                v-model="frequency"
                min="1"
                :step="100"
            />

            <!-- Distance Slider -->
            <HoloSlider
                label="Distance (km)"
                :log="true"
                unit="km"

                v-model="distance"
                :min="0.1"
                :max="100"
            />

            <!-- Transmission Power Slider -->
            <HoloSlider
                label="Antenna Power (dBm)"
                unit="dBm"

                v-model="power"
                :min="0"
                :max="70"
                step="1"
            />

            <!-- Cyclic Prefix Mode Selection -->
            <HoloSelect
                label="Cyclic Prefix Mode"

                v-model="mode"
                :items="[
                    { title: 'Normal',   value: 1 },
                    { title: 'Extended', value: 6/7 },
                ]"
            />
        </template>

        <template #output-1>
            <div style="height: 20px;"></div>

            <!-- Network status -->
            <VContainer>
                <VRow>
                    <VCol cols="6" class="pa-0 pr-3">
                        <NetworkBars
                            :value="
                                sinr?.snr >= 25 ? 5 :
                                sinr?.snr >= 20 ? 4 :
                                sinr?.snr >= 15 ? 3 :
                                sinr?.snr >= 10 ? 2 :
                                sinr?.snr >= 0  ? 1 :
                                0"
                            :max="5"
                        />
                    </VCol>

                    <VCol cols="6" class="pa-0 d-flex flex-column justify-center">
                        <div class="sinr">
                            <span class="strong">{{ sinr?.snr.toFixed(1) ?? '0.0' }}</span>
                            (<span class="weak">{{ (rcvPower - NOISE_INTERFERENCE).toFixed(1) }} dB</span>)
                        </div>
                        <div class="modulation">
                            <span class="strong">{{ sinr?.mod ?? 'QPSK' }}</span>
                            (<span class="weak">{{ sinr?.code ?? 'Fail' }}</span>)
                        </div>
                    </VCol>
                </VRow>
            </VContainer>

            <div style="min-height: 20px; flex-grow: 1;"></div>

            <!-- Transmission Stats -->
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

            <div class="d-flex justify-center">
                <!-- Throughput Gauge -->
                <Gauge
                    :percent="(throughput / maxThroughput * 100)"
                    :value="`${throughput.toFixed(1)} Mbps`"
                />
            </div>

            <div style="min-height: 20px; flex-grow: 1;"></div>

            <!-- Efficiency Stats -->
            <DataList
                class="pa-0"
                :items="[
                    {
                        title: 'Spectral Efficiency',
                        value: sinr ? sinr.eff : '0.00'
                    },
                    {
                        title: 'Useful bits',
                        value: sinr ?
                            `${(100 * sinr.eff / (sinr.eff + 1)).toFixed(2)} %` :
                            '0.00 %'
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