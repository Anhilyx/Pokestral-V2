<script setup>
    import { useAttrs } from 'vue';

    const model = defineModel({});
    const attrs = useAttrs();

    defineOptions({
        inheritAttrs: false
    });
</script>

<template>
    <HoloInput class="holo-switch">
        <VSwitch
            v-model="model"
            v-bind="$attrs"
            
            variant="outlined"
            density="comfortable"
            :hide-details="true"
        >
            <template #label>
                <slot></slot>
            </template>
        </VSwitch>
    </HoloInput>
</template>

<style scoped>
    /***** Thumb *****/
    :deep(.v-switch__thumb) {
        /* Background */
        background: var(--holo-input__thumb-color-2) !important;

        /* Glow effect */
        box-shadow: var(--holo-input__thumb-glow-2) !important;
    }

    /***** Background *****/
    :deep(:not(.v-selection-control--dirty) .v-switch__track) {
        /* Background */
        background: var(--holo-input__empty-color-2) !important;

        /* Glow effect */
        box-shadow: var(--holo-input__empty-glow-2) !important;
    }
    :deep(.v-selection-control--dirty .v-switch__track) {
        /* Background */
        background: var(--holo-input__fill-color-2) !important;

        /* Glow effect */
        box-shadow: var(--holo-input__fill-glow-2) !important;
    }

    /***** Text *****/
    :deep(:not(.v-selection-control--dirty) .v-label) {
        /* Background */
        color: var(--holo-theme__text-color-muted) !important;

        /* Glow effect */
        text-shadow: 0 0 0px var(--holo-theme__text-color-muted) !important;
    }
    :deep(.v-selection-control--dirty .v-label) {
        /* Background */
        color: var(--holo-theme__text-color-accentued) !important;

        /* Glow effect */
        text-shadow: 0 0 var(--holo-theme__glow-strength-text-medium) var(--holo-theme__text-color-accentued) !important;
    }

    /***** On hover *****/
    :deep(.v-selection-control:hover) {
        /* Backgrounds */
        --holo-input__empty-color-2: var(--holo-input__empty-color-2-hover);
        --holo-input__fill-color-2:  var(--holo-input__fill-color-2-hover);
        --holo-input__thumb-color-2: var(--holo-input__thumb-color-2-hover);

        /* Glow */
        --holo-input__empty-glow-2:  var(--holo-input__empty-glow-2-hover);
        --holo-input__fill-glow-2:   var(--holo-input__fill-glow-2-hover);
        --holo-input__thumb-glow-2:  var(--holo-input__thumb-glow-2-hover);
    }
</style>