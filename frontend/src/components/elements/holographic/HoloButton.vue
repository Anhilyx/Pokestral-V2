<script setup>
    const model = defineModel({});

    defineOptions({
        inheritAttrs: false
    });
</script>

<template>
    <HoloInput class="holo-button d-flex justify-center">
        <VBtn
            v-model="model"
            v-bind="$attrs"
           
            variant="plain"
            :hide-details="true"
        >
            <slot name="default"></slot>
        </VBtn>
    </HoloInput>
</template>

<style scoped>
    /* Variables */
    .holo-button {
        --holo-button__border-width: 10px;
        --holo-button__border-glow-weak-base:     calc(var(--holo-button__border-width) / 2 * 1.0);
        --holo-button__border-glow-weak-spread:   calc(var(--holo-button__border-width) / 2 * 0.2);
        --holo-button__border-glow-strong-base:   calc(var(--holo-button__border-width) / 2 * 0.5);
        --holo-button__border-glow-strong-spread: calc(var(--holo-button__border-width) / 2 * 0.1);
        --holo-button__border-glow-weak: var(--holo-button__border-glow-weak-base) var(--holo-button__border-glow-weak-spread);
        --holo-button__border-glow-strong: var(--holo-button__border-glow-strong-base) var(--holo-button__border-glow-strong-spread);
    }

    :deep(button) {
        /* Background */
        background: var(--holo-theme__background-color) !important;

        /* Borders */
        box-shadow:       0 0 var(--holo-button__border-glow-weak)   var(--holo-theme__glow-bright-weak),
                          0 0 var(--holo-button__border-glow-strong) var(--holo-theme__glow-bright-strong),
                    inset 0 0 var(--holo-button__border-glow-weak)   var(--holo-theme__glow-bright-weak),
                    inset 0 0 var(--holo-button__border-glow-strong) var(--holo-theme__glow-bright-strong);
    }

    /* On hover */
    :deep(.v-btn__underlay:hover) {
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

    /***** Spinner *****/

    /* Remove default spinners for number inputs */
    :deep(.v-field__input::-webkit-inner-spin-button),
    :deep(.v-field__input::-webkit-outer-spin-button) {
        -webkit-appearance: none;
        margin: 0;
    }

    .holo-text-field__spinner {
        /* Layout */
        display: flex;
        flex-direction: column;

        /* Show/Hide */
        opacity: 0;
        transition: opacity var(--animation-speed-fast);
    }

    .holo-button:hover .holo-text-field__spinner {
        /* Show/Hide */
        opacity: 1;
    }

    .holo-text-field__spinner-arrow-up,
    .holo-text-field__spinner-arrow-down {
        /* Size */
        height: calc(var(--holo-text-field__spinner-height) / 2);
       
        /* Layout */
        display: flex;
        overflow: hidden;

        /* Interaction */
        cursor: pointer;

        /* Animation */
        color:                                                         var(--holo-text-field__spinner-color);
        text-shadow: 0 0 var(--holo-text-field__spinner-glow-strength) var(--holo-text-field__spinner-color);
        transition: color var(--animation-speed-fast),
                    text-shadow var(--animation-speed-fast);
    }

    /* On hover */
    .holo-text-field__spinner-arrow-up:hover,
    .holo-text-field__spinner-arrow-down:hover {
        --holo-text-field__spinner-color: var(--holo-theme__text-color-accentued);
        --holo-text-field__spinner-glow-strength: var(--holo-theme__glow-strength-text-medium);
    }
   
    /* Fix icon base shape (lot of empty space) */
    .holo-text-field__spinner-arrow-up {
        /* Layout */
        align-items: start;
    }
    .holo-text-field__spinner-arrow-down {
        /* Layout */
        align-items: end;
    }
</style>