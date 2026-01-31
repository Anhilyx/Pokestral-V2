<script setup>
    import { computed } from 'vue';

    const props = defineProps({
        min: {
            type: Number,
            default: 1,
            validator: (value) => value > 0
        },
        max: {
            type: Number,
            default: 100,
            validator: (value) => value > 0
        },
        allowZero: {
            type: Boolean,
            default: false
        },

        precision: {
            type: Number,
            default: 100
        },

        step: {}  // Capture step but ignore it
    });

    const model = defineModel({
        type: Number,
        required: true
    });

    const min = computed(() => Math.log10(props.min));
    const max = computed(() => Math.log10(props.max));
    const step = computed(() => {
        return (max.value - min.value) / props.precision;
    });

    const value = computed({
        get() {
            // Handle underflow
            if (model.value < props.min)
                return props.allowZero ?
                    min.value - step.value :
                    min.value;
            
            // Handle overflow
            else if (model.value > props.max)
                return max.value;
            
            // Normal case
            return Math.log10(model.value);
        },

        set(val) {
            // Allow zeroing
            if (val < min.value)
                model.value = 0;

            // Normal case
            else
                model.value = Math.pow(10, val);
        }
    });
</script>

<template>
    <VSlider
        class="log-slider"
        v-model="value"
        :min="allowZero ? min - step : min"
        :max="max"
        :step="step"
    >
        <template #thumb-label>
            <slot name="thumb-label" :modelValue="model">
                {{ model.toFixed(2) }}
            </slot>
        </template>
    </VSlider>
</template>