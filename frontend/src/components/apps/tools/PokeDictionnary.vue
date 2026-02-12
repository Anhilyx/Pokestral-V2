<script setup>
    import { ref } from 'vue';
    import { getDefinition } from '@/services/tools';

    const name = ref('');
    const category = ref(null);

    const result = ref(undefined);
    const error = ref(undefined);

    async function askDefinition() {
        try {
            const res = await getDefinition(name.value, category.value);

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
</script>

<template>
    <HoloApp title="Dictionnary">

        <template #input>
            <HoloTextField
                label="Move/Ability name"
                placeholder="Encore"

                v-model="name"
                @blur="askDefinition()"
            />

            <HoloSelect
                label="Category"

                v-model="category"
                @update:model-value="askDefinition()"
                :items="[
                    { title: '???',     value: null      },
                    { title: 'Move',    value: 'move'    },
                    { title: 'Ability', value: 'ability' },
                    { title: 'Item',    value: 'item'    },
                ]"
            />
        </template>

        <template #output-1>
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
            <div v-else class="dictionnary__output-json">
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
    :deep(textarea) {
        font-family: 'Courier New', Courier, monospace;
    }
</style>