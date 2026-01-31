<script setup>
    import { ref, computed } from 'vue';

    const isOn = defineModel();

    const props = defineProps({
        name: {
            type: String,
            required: true,
        },

        height: {
            type: Number,
            default: undefined,
        },
    });

    const emits = defineEmits([
        'update'
    ]);

    // Compute height of chip automatically
    const el = ref(null);
    const height = computed(() => {
        // Return prop if set
        if (props.height)
            return props.height;

        // Skip if not mounted
        if (!el.value)
            return 0;

        return parseInt(
            getComputedStyle(el.value)
            .getPropertyValue('--app-chip__height')
            .replace('px', '')
        );
    });

    function toggle() {
        isOn.value = !isOn.value;
        emits('update', !isOn.value);
    }
</script>

<template>
    <div
        ref="el"
        class="app-chip no-select"
        :class="isOn ? 'on' : 'off'"
        :style="{
            '--app-chip__height': props.height ? `${props.height}px` : undefined
        }"
        @click="toggle()"
    >
        <!-- Text -->
        <div class="app-chip__text nowrap">
            {{ name }}
        </div>

        <!-- Icon -->
        <div class="app-chip__icon-container">

            <!-- Two icons + opacity allow for smooth transition between one another -->
            <div class="app-chip__icon-layout">
                <Icon
                    icon="check_circle"
                    :size="height - 4"
                    :style="{
                        opacity: isOn ? 1 : 0
                    }"
                />
            </div>
            <div class="app-chip__icon-layout">
                <Icon
                    icon="cancel"
                    :size="height - 4"
                    :style="{
                        opacity: isOn ? 0 : 1
                    }"
                />
            </div>
        </div>
    </div>
</template>

<style scoped>
    /* Variables */
    .app-chip {
        /* Layout */
        --app-chip__height: 40px;
        --app-chip__icon-margin: 2px;

        /* Colors */
        --app-chip__chip-color-background-on:  var(--container-background-filled);
        --app-chip__chip-color-background-off: var(--container-background-empty);
        --app-chip__chip-color-icon-background-on:  color-mix(in srgb, black, transparent 88%);
        --app-chip__chip-color-icon-background-off: color-mix(in srgb, black, transparent 82%);

        --app-chip__chip-color-text-on:  color-mix(in srgb, white, transparent  0%);
        --app-chip__chip-color-text-off: color-mix(in srgb, white, transparent 40%);
        --app-chip__chip-color-icon-on:  color-mix(in srgb, white, transparent 30%);
        --app-chip__chip-color-icon-off: color-mix(in srgb, white, transparent 60%);

        /* States */
        --app-chip__overlay-hover: color-mix(in srgb, white, transparent 85%);
        --app-chip__overlay-click:   color-mix(in srgb, white, transparent 65%);
    }

    .app-chip {
        /* Shape */
        width: fit-content;
        height: var(--app-chip__height);
        border-radius: calc(var(--app-chip__height) / 2);

        /* Layout */
        display: flex;

        /* Style */
        cursor: pointer;

        /* Animation */
        transition: all var(--animation-speed-fast);
        
        /* Event handling */
        position: relative;
    }

    /***** Text *****/

    .app-chip__text {
        /* Layout */
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 15px;

        /* Style */
        font-size: 20px;
        font-weight: bold;
    }

    /***** Icon *****/

    .app-chip__icon-container {
        /* Shape */
        width: var(--app-chip__height);
        height: var(--app-chip__height);
        border-radius: 50%;

        /* Layout */
        position: relative;
    }

    .app-chip__icon-layout {
        /* Overlap icons */
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;

        /* Layout */
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .icon {
        /* Animation */
        transition: all var(--animation-speed-fast);
    }

    /***** States *****/

    /* On state */
    .app-chip.on {
        background-color: var(--app-chip__chip-color-background-on);
        color: var(--app-chip__chip-color-text-on);
    }
    .app-chip.on .app-chip__icon-container {
        background-color: var(--app-chip__chip-color-icon-background-on);
        color: var(--app-chip__chip-color-icon-on);
    }
    
    /* Off state */
    .app-chip.off {
        background-color:    var(--app-chip__chip-color-background-off);
        color: var(--app-chip__chip-color-text-off);
    }
    .app-chip.off .app-chip__icon-container {
        background-color: var(--app-chip__chip-color-icon-background-off);
        color: var(--app-chip__chip-color-icon-off);
    }

    /* Hover / Active Effects */
    .app-chip::after {
        content: '';

        /* Position above */
        position: absolute;
        inset: 0;
        z-index: 1;

        /* Rounded */
        border-radius: inherit;

        /* Prevent interaction */
        pointer-events: none;

        /* Animation */
        transition: all var(--animation-speed-fast);
    }

    .app-chip:hover::after {
        background-color: var(--app-chip__overlay-hover);
    }
    .app-chip:active::after {
        background-color: var(--app-chip__overlay-click);
    }
</style>