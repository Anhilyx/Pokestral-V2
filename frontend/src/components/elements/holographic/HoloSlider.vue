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

        /* Colors */
        --holo-slider__empty-color: color-mix(in srgb, var(--holo-theme__background-color-off), transparent                          70%);
        --holo-slider__fill-color:  color-mix(in srgb, var(--holo-theme__background-color),     transparent                          50%);
        --holo-slider__thumb-color: color-mix(in srgb, var(--holo-theme__background-color),     var(--holo-theme__glow-medium-color) 20%);
        
        --holo-slider__empty-color-hover: color-mix(in srgb, var(--holo-theme__background-color-off), transparent                          70%);
        --holo-slider__fill-color-hover:  color-mix(in srgb, var(--holo-theme__background-color),     transparent                          30%);
        --holo-slider__thumb-color-hover: color-mix(in srgb, var(--holo-theme__background-color),     var(--holo-theme__glow-medium-color) 35%);
        
        --holo-slider__empty-color-focus: color-mix(in srgb, var(--holo-theme__background-color-off), transparent                           70%);
        --holo-slider__fill-color-focus:  color-mix(in srgb, var(--holo-theme__background-color),     transparent                           10%);
        --holo-slider__thumb-color-focus: color-mix(in srgb, var(--holo-theme__background-color),     var(--holo-theme__glow-medium-color) 100%);

        /* Glow */
        --holo-slider__thumb-glow-multiplier: 2;

        --holo-slider__empty-glow: 0 0 0px                                                                                    var(--holo-slider__empty-color);
        --holo-slider__fill-glow:  0 0 var(--holo-theme__glow-strength-low)                                                   var(--holo-input__glow-color);
        --holo-slider__thumb-glow: 0 0 calc(var(--holo-theme__glow-strength-low) * var(--holo-slider__thumb-glow-multiplier)) var(--holo-input__glow-color);

        --holo-slider__empty-glow-hover: 0 0 0px                                                                                      var(--holo-slider__empty-color);
        --holo-slider__fill-glow-hover:  0 0 var(--holo-theme__glow-strength-medium)                                                   var(--holo-input__glow-color);
        --holo-slider__thumb-glow-hover: 0 0 calc(var(--holo-theme__glow-strength-medium) * var(--holo-slider__thumb-glow-multiplier)) var(--holo-input__glow-color);

        --holo-slider__empty-glow-focus: 0 0 0px                                                                                     var(--holo-slider__empty-color);
        --holo-slider__fill-glow-focus:  0 0 var(--holo-theme__glow-strength-high)                                                   var(--holo-input__glow-color);
        --holo-slider__thumb-glow-focus: 0 0 calc(var(--holo-theme__glow-strength-high) * var(--holo-slider__thumb-glow-multiplier)) var(--holo-input__glow-color);
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
        background: var(--holo-slider__empty-color) !important;

        /* Glow */
        box-shadow: var(--holo-slider__empty-glow) !important;
    }

    :deep(.v-slider-track__fill) {
        /* Background */
        background: var(--holo-slider__fill-color) !important;

        /* Glow */
        box-shadow: var(--holo-slider__fill-glow) !important;
    }

    :deep(.v-slider-thumb__surface) {
        /* Background */
        background: var(--holo-slider__thumb-color) !important;

        /* Glow */
        box-shadow: var(--holo-slider__thumb-glow) !important;
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
        --holo-slider__empty-color: var(--holo-slider__empty-color-hover);
        --holo-slider__fill-color:  var(--holo-slider__fill-color-hover);
        --holo-slider__thumb-color: var(--holo-slider__thumb-color-hover);

        /* Glow */
        --holo-slider__empty-glow:  var(--holo-slider__empty-glow-hover);
        --holo-slider__fill-glow:   var(--holo-slider__fill-glow-hover);
        --holo-slider__thumb-glow:  var(--holo-slider__thumb-glow-hover);
    }

    :deep(.v-slider--focused) {
        /* Backgrounds */
        --holo-slider__empty-color: var(--holo-slider__empty-color-focus);
        --holo-slider__fill-color:  var(--holo-slider__fill-color-focus);
        --holo-slider__thumb-color: var(--holo-slider__thumb-color-focus);

        /* Glow */
        --holo-slider__empty-glow:  var(--holo-slider__empty-glow-focus);
        --holo-slider__fill-glow:   var(--holo-slider__fill-glow-focus);
        --holo-slider__thumb-glow:  var(--holo-slider__thumb-glow-focus);
    }
</style>