<script setup>
    import { onMounted, ref } from 'vue';
    import { getTypesTable as fetchTypesTable, getSpecificTypeTable as fetchSpecificTypeTable, getPokemonTypeTable as fetchPokemonTypeTable } from '@/services/tools';

    const nameRef = ref('');
    const name = ref('');
    const specific = ref(false);
    const types = ref(undefined);

    const result = ref(undefined);
    const error = ref(undefined);

    async function getTypesTable() {
        name.value = nameRef.value.trim();

        try {
            const res = await fetchTypesTable();

            // Store results
            result.value = res.data;
            types.value = Object.keys(res.data);
            error.value = undefined;
            console.log(res.data);
        }
       
        // Error case
        catch (err) {
            console.error(err);
            result.value = undefined;
            error.value = err;
        }
    }

    async function getSpecificTypeTable() {
        name.value = nameRef.value.trim();

        // Retrieve types table first to get all the different types (and their order)
        if (types.value === undefined) {
            try {
                const res = await fetchTypesTable();
                types.value = Object.keys(res.data);
            } catch (err) {
                console.error(err);
                result.value = undefined;
                error.value = err;
            }
        }

        try {
            let res;
            if (types.value.includes(name.value[0].toUpperCase() + name.value.slice(1).toLowerCase())) {
                res = await fetchSpecificTypeTable(name.value);
            } else {
                res = await fetchPokemonTypeTable(name.value);
            }

            // Store results
            result.value = res.data;
            error.value = undefined;
            console.log(res.data);
        }
       
        // Error case
        catch (err) {
            console.error(err);
            result.value = undefined;
            error.value = err;
        }
    }

    function formatTypesTableResult(data) {
        const firstValue = Object.values(data)[0];
        const isAlreadyFormatted = typeof firstValue === 'object' && firstValue !== null;

        if (!isAlreadyFormatted) {
            let targetKeys;
            
            const formattedName = name.value.charAt(0).toUpperCase() + name.value.slice(1).toLowerCase();

            if (types.value.includes(formattedName)) {
                targetKeys = [formattedName];
            } else {
                targetKeys = Object.keys(result.value.attacking);
            }

            const formattedData = {};
            for (const targetKey of targetKeys) {
                formattedData[targetKey] = { ...data };
            }
            return formattedData;
        }

        console.log(data)
        return data;
    }

    onMounted(() => {
        getTypesTable();
    });
</script>

<template>
    <HoloApp
        title="Types Table"
        :outputs="2"
    >

        <template #input>
            <HoloSwitch v-model="specific" @update:model-value="specific ? (name !== '' ? getSpecificTypeTable() : '') : getTypesTable()">
                Specific Pokemon/Type
            </HoloSwitch>
            <HoloTextField
                v-if="specific"
                label="Pokemon/Type name"
                placeholder="Charizard"

                v-model="nameRef"
                @blur="getSpecificTypeTable()"
            />
        </template>

        <template #output-1>
            <!-- Show loading if no result -->
            <div
                v-if="!(result ?? false)"
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

            <!-- Else show result -->
            <div v-if="result ?? false">
                <!-- If the types table contains an attacker and a defender -->
                <div v-if="Object.keys(result).includes('attacking') && Object.keys(result).includes('defending')"
                    class="d-flex flex-column align-center"
                >
                    <TypesTableTable
                        :values="formatTypesTableResult(result.attacking)"
                        :types="types"
                        class="mb-4"
                    />
                    <TypesTableTable
                        :values="formatTypesTableResult(result.defending)"
                        :types="types"
                        :invert="true"
                    />
                </div>

                <div v-else
                    class="d-flex justify-center"
                >
                    <TypesTableTable :values="formatTypesTableResult(result)" :types="types" />
                </div>
            </div>
        </template>

        <template #output-2>
            <!-- Show loading if nothing -->
            <div
                v-if="!(result ?? false) && !(error ?? false)"
                class="d-flex justify-center"
            >
                <VProgressCircular
                    color="var(--holo-theme__background-color)"
                    size="64" width="6"
                    indeterminate
                />
            </div>

            <!-- Else show error/result -->
            <div v-else class="damage-calculator__output-json">
                <HoloTextArea
                    class="monospace"
                    :label="result ? 'Result JSON' : 'Error Message'"
                    :model-value="JSON.stringify(result ?? error, null, 1)"
                    readonly
                />
            </div>
        </template>
    </HoloApp>
</template>

<style scoped>
    /* Use a monospace font for the attacker set & JSON output */
    :deep(.monospace textarea),
    :deep(.monospace input) {
        font-family: 'Courier New', Courier, monospace;
    }

    /* Force output-2 textarea to take full height */
    /* (In a very beautifyl and elegant way ;) ) */
    .damage-calculator__output-json,
    .damage-calculator__output-json > *,
    .damage-calculator__output-json > * > *,
    .damage-calculator__output-json > * > * > *,
    .damage-calculator__output-json > * > * > * > * {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
</style>