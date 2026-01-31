<script setup>
    import { useAttrs } from 'vue';

    const model = defineModel({});
    const attrs = useAttrs();

    defineOptions({
        inheritAttrs: false
    });
</script>

<template>
    <HoloInput class="holo-text-area">
        <VTextarea
            v-model="model"
            v-bind="$attrs"
            
            variant="outlined"
            density="comfortable"
            :hide-details="true"
        >
            <template #append-inner>
                <div v-if="attrs.type === 'number'" class="arrow-container">
                    <div
                        @click="model += 1"
                        class="arrow"
                    >
                        <Icon icon="arrow_drop_up" :size="32" />
                    </div>

                    <div
                        @click="model -= 1"
                        class="arrow"
                    >
                        <Icon icon="arrow_drop_down" :size="32" />
                    </div>
                </div>
            </template>
        </VTextarea>
    </HoloInput>
</template>

<style scoped>
    .holo-text-area {
        /* Compensate for label */
        padding-top: calc(var(--holo-input__label-height) / 2);
    }

    .v-textarea {
        /* Background */
        background: var(--holo-input__background-color) !important;

        /* Glow effect */
        box-shadow: var(--holo-input__glow) !important;
    }

    /* On hover */
    .v-textarea:hover {
        /* Background */
        background: var(--holo-input__background-color-hover) !important;

        /* Glow effect */
        box-shadow: var(--holo-input__glow-hover) !important;
    }

    /* On focus */
    :deep(.v-field--focused) {
        /* Background */
        background: var(--holo-input__background-color-focus) !important;

        /* Glow effect */
        box-shadow: var(--holo-input__glow-focus) !important;
    }

    :deep(textarea) {
        /* Hide resize handle */
        resize: none;

        /* Hide scrollbar */
        scrollbar-width: none;
        -ms-overflow-style: none;
    }
    /* Hide scrollbar */
    :deep(textarea::-webkit-scrollbar) {
        display: none;
    }
</style>