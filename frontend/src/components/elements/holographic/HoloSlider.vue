<script setup>
    const model = defineModel({});

    const props = defineProps({
        label: {
            type: String,
            default: null
        },

        log: {
            type: Boolean,
            default: false
        },
        unit: {
            type: String,
            default: null
        },

        format: {  // How will the value be formatted
            type: Function,
            default: null
        },

        thumbLabel: {
            type: [Boolean, String],
            default: true
        }
    });

    function formatLog(value) {
        return value.toFixed(
            value === 0 ? 2 :
            Math.max(0, 1 - Math.floor(Math.log10(value)))
        );
    }

    defineOptions({
        inheritAttrs: false
    });
</script>

<template>
    <HoloInput class="holo-slider">
        <div class="holo-slider__label">
            <div v-if="props.label" class="weak"> {{ props.label }} </div>
            <VSpacer />
            <div class="strong"> {{
                props.format ?
                format(model) :
                log ?
                formatLog(model) :
                model
            }} {{ props.unit ?? '' }} </div>
        </div>
       
        <LogSlider v-if="props.log"
            v-model="model"
            v-bind="$attrs"

            variant="outlined"
            :thumb-label="props.thumbLabel"
            :hide-details="true"
        >
            <template #thumb-label="{ modelValue }">
                <span style="white-space: nowrap">
                    {{ format ? format(modelValue) : formatLog(modelValue) }}
                    <span v-if="props.unit"> {{ props.unit }} </span>
                </span>
            </template>
        </LogSlider>

        <VSlider v-else
            v-model="model"
            v-bind="$attrs"

            variant="outlined"
            :thumb-label="props.thumbLabel"
            :hide-details="true"
        >
            <template #thumb-label="{ modelValue }">
                <span style="white-space: nowrap">
                    {{ format ? format(modelValue) : modelValue }}
                    <span v-if="props.unit"> {{ props.unit }} </span>
                </span>
            </template>
        </VSlider>
    </HoloInput>
</template>

<style scoped>
    /* Variables */
    .holo-slider {
        /* Layout */
        --holo-slider__thumb-offset-effect: -4px;

        /* Glow */
        --holo-slider__thumb-glow-multiplier: 2;
    }

    .holo-slider {
        /* Special offset, as the thumb makes the element look shorter than it actually is */
        margin-bottom: var(--holo-slider__thumb-offset-effect);
    }

    .holo-slider__label {
        /* Layout */
        display: flex;
        align-items: end;
    }

    :deep(.v-slider-track) {
        /* Background */
        background: var(--holo-input__empty-color-2) !important;

        /* Glow */
        box-shadow: var(--holo-input__empty-glow-2) !important;
    }

    :deep(.v-slider-track__fill) {
        /* Background */
        background: var(--holo-input__fill-color-2) !important;

        /* Glow */
        box-shadow: var(--holo-input__fill-glow-2) !important;
    }

    :deep(.v-slider-thumb__surface) {
        /* Background */
        background: var(--holo-input__thumb-color-2) !important;

        /* Glow */
        box-shadow: var(--holo-input__thumb-glow-2) !important;
    }

    /* Thumb Label (if on) */
    :deep(.v-slider-thumb__label) {
        /* Text */
        color: var(--holo-theme__text-color-base) !important;

        /* Background */
        background: var(--holo-theme__background-color-transparency-low) !important;

        /* Glow */
        box-shadow: 0 0 var(--holo-theme__glow-strength-medium) var(--holo-theme__glow-medium-weak) !important;
    }

    :deep(.v-slider:hover:not(.v-slider--focused)) {
        /* Backgrounds */
        --holo-input__empty-color-2: var(--holo-input__empty-color-2-hover);
        --holo-input__fill-color-2:  var(--holo-input__fill-color-2-hover);
        --holo-input__thumb-color-2: var(--holo-input__thumb-color-2-hover);
       
        /* Glow */
        --holo-input__empty-glow-2:  var(--holo-input__empty-glow-2-hover);
        --holo-input__fill-glow-2:   var(--holo-input__fill-glow-2-hover);
        --holo-input__thumb-glow-2:  var(--holo-input__thumb-glow-2-hover);
    }

    :deep(.v-slider--focused) {
        /* Backgrounds */
        --holo-input__empty-color-2: var(--holo-input__empty-color-2-focus);
        --holo-input__fill-color-2:  var(--holo-input__fill-color-2-focus);
        --holo-input__thumb-color-2: var(--holo-input__thumb-color-2-focus);

        /* Glow */
        --holo-input__empty-glow-2:  var(--holo-input__empty-glow-2-focus);
        --holo-input__fill-glow-2:   var(--holo-input__fill-glow-2-focus);
        --holo-input__thumb-glow-2:  var(--holo-input__thumb-glow-2-focus);
    }
</style>