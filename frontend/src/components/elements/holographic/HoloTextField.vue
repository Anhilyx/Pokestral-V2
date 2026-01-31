<script setup>
    import { useAttrs } from 'vue';

    const model = defineModel({});
    const attrs = useAttrs();

    defineOptions({
        inheritAttrs: false
    });
</script>

<template>
    <HoloInput class="holo-text-field">
        <VTextField
            v-model="model"
            v-bind="$attrs"
            
            variant="outlined"
            density="comfortable"
            :hide-details="true"
            autocomplete="off"
        >
            <template #append-inner>
                <div v-if="attrs.type === 'number'" class="holo-text-field__spinner">
                    <div
                        @click="() => {
                            let value = model + (attrs.step ? Number(attrs.step) : 1);
                            if (attrs.max !== undefined && value > Number(attrs.max)) {
                                value = Number(attrs.max);
                            }
                            model = value;
                        }"
                        class="holo-text-field__spinner-arrow-up"
                    >
                        <Icon icon="arrow_drop_up" :size="32" />
                    </div>

                    <div
                        @click="() => {
                            let value = model - (attrs.step ? Number(attrs.step) : 1);
                            if (attrs.min !== undefined && value < Number(attrs.min)) {
                                value = Number(attrs.min);
                            }
                            model = value;
                        }"
                        class="holo-text-field__spinner-arrow-down"
                    >
                        <Icon icon="arrow_drop_down" :size="32" />
                    </div>
                </div>
            </template>
        </VTextField>
    </HoloInput>
</template>

<style scoped>
    /* Variables */
    .holo-text-field {
        /* Spinner */
        --holo-text-field__spinner-color: var(--holo-theme__text-color-muted);

        --holo-text-field__spinner-height: 48px;
        --holo-text-field__spinner-glow-strength: 0px;
    }

    .holo-text-field {
        /* Compensate for label */
        padding-top: calc(var(--holo-input__label-height) / 2);
    }

    .v-text-field {
        /* Background */
        background: var(--holo-input__background-color) !important;

        /* Glow effect */
        box-shadow: var(--holo-input__glow) !important;
    }

    /* On hover */
    .v-text-field:hover {
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

    .holo-text-field:hover .holo-text-field__spinner {
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