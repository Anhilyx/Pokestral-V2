<script setup>
    import { ref, computed } from 'vue';

    const props = defineProps({
        /* Theme */
        theme: {
            type: String,
            default: null,
            validator: (value) => [
                'default', 'pokeball',
                null, undefined
            ].includes(value)
        },

        /* Options */
        options: {
            type: Array,
            default: [],
            validator: (value) => value.every(
                (option) => [
                    'simplified',
                ].includes(option)
            )
        }
    });

    // Check if theme was loaded at least once
    const el = ref(null);
    const isLoaded = computed(() => {
        if (!el.value) return false;

        return getComputedStyle(el.value.parentElement)
              .getPropertyValue('--holo-theme__loaded');
    });

    defineOptions({
        inheritAttrs: false
    });
</script>

<template>
    <div
        ref="el"
        v-bind="$attrs"
        class="holo-theme"
        :class="{
            // Variables
            'holo-theme__values': !isLoaded || props.theme === 'default',

            // Themes
            'holo-theme__theme-pokeball': props.theme === 'pokeball',

            // Options
            'holo-theme__option-simplified': props.options.includes('simplified'),
        }"
    >
        <slot></slot>
    </div>
</template>

<style scoped>
    /************
    | Variables |
    ************/

    .holo-theme__values {
        /* Loaded indicator */
        --holo-theme__loaded: 1;

        /* Div dimensions */
        --holo-theme__box-border-width: 20px;

        /* App background */
        --holo-theme__app-background-base: hsl(0, 0%, 2%);
        --holo-theme__app-background-effect: linear-gradient(       var(--holo-theme__app-background-effect-color) 1px, transparent 1px),
			                                 linear-gradient(90deg, var(--holo-theme__app-background-effect-color) 1px, transparent 1px);
        --holo-theme__app-background-effect-color: hsla(168, 100%, 50%, 0.1);
        --holo-theme__app-background-effect-size: 40px;
        --holo-theme__app-background-animation-speed: 0.25;  /* Pixels per second */

        /* Background colors */
        --container-background-filled: hsl(190, 100%, 30%);

        --holo-theme__background-color: var(--container-background-filled);
        --holo-theme__background-color-transparency-high:   color-mix(in srgb, var(--holo-theme__background-color), transparent 90%);
        --holo-theme__background-color-transparency-medium: color-mix(in srgb, var(--holo-theme__background-color), transparent 60%);
        --holo-theme__background-color-transparency-low:    color-mix(in srgb, var(--holo-theme__background-color), transparent 20%);
        --holo-theme__background: var(--holo-theme__background-color);
        --holo-theme__background-opacity-low: 0.1;
        --holo-theme__background-opacity-medium: 0.4;
        --holo-theme__background-opacity-high: 0.8;

        --holo-theme__background-color-off: var(--container-background-empty);
        --holo-theme__background-color-off-transparency-high:   color-mix(in srgb, var(--holo-theme__background-color-off), transparent 90%);
        --holo-theme__background-color-off-transparency-medium: color-mix(in srgb, var(--holo-theme__background-color-off), transparent 70%);
        --holo-theme__background-color-off-transparency-low:    color-mix(in srgb, var(--holo-theme__background-color-off), transparent 30%);
        --holo-theme__background-off: var(--holo-theme__background-color-off);
        --holo-theme__background-off-opacity-low: 0.1;
        --holo-theme__background-off-opacity-medium: 0.3;
        --holo-theme__background-off-opacity-high: 0.7;

        --holo-theme__blur-strength-low: 4px;
        --holo-theme__blur-strength-medium: 8px;
        --holo-theme__blur-strength-high: 16px;

        /* Glow colors */
        --holo-theme__glow-bright-color: hsl(203, 100%, 86%);
        --holo-theme__glow-bright-strong: color-mix(in srgb, var(--holo-theme__glow-bright-color), transparent  0%);
        --holo-theme__glow-bright-weak:   color-mix(in srgb, var(--holo-theme__glow-bright-color), transparent 60%);

        --holo-theme__glow-medium-color: hsl(190, 100%, 50%);
        --holo-theme__glow-medium-strong: color-mix(in srgb, var(--holo-theme__glow-medium-color), transparent  0%);
        --holo-theme__glow-medium-weak:   color-mix(in srgb, var(--holo-theme__glow-medium-color), transparent 60%);

        --holo-theme__glow-strength-low: 3px;
        --holo-theme__glow-strength-medium: 5px;
        --holo-theme__glow-strength-high: 15px;
        --holo-theme__glow-strength-text-low: 4px;
        --holo-theme__glow-strength-text-medium: 8px;
        --holo-theme__glow-strength-text-high: 16px;

        /* Text color */
        --holo-theme__text-color-base: rgb(224, 224, 224);
        --holo-theme__text-color-accentued: rgb(255, 255, 255);
        --holo-theme__text-color-muted: rgba(224, 224, 224, 0.85);
    }

    /*********
    | Styles |
    *********/

    /***** VApp *****/

    :deep(.v-application) {
        /* Base text color */
        color: var(--holo-theme__text-color-base);

		/* Background effect */
		background-color: var(--holo-theme__app-background-base);
		background-image: var(--holo-theme__app-background-effect);
		background-size: var(--holo-theme__app-background-effect-size) var(--holo-theme__app-background-effect-size);
       
        /* Background animation */
        animation: app-background-animation
                   calc(var(--holo-theme__app-background-effect-size) / 1px / var(--holo-theme__app-background-animation-speed) * 1s)
                   linear infinite;
    }

    /* Infinite rolling background animation */
    @keyframes app-background-animation {
        from {
            background-position: 0px 0px;
        }
        to {
            background-position: var(--holo-theme__app-background-effect-size) var(--holo-theme__app-background-effect-size);
        }
    }

    /***** DataList *****/

    :deep(.data-list__row) {
        /* Separator style */
        border-image: linear-gradient(90deg,
            transparent                 0%,
            var(--holo-theme__glow-bright-strong)  30%,
            var(--holo-theme__glow-bright-weak)    70%,
            transparent               100%
        );
        border-image-slice: 1;
    }

    /* Custom hover effect */
    :deep(.data-list__row::after) {
        inset: 5px !important;
        border-radius: 25% !important;
        box-shadow: 0 0 5px color-mix(in srgb, var(--holo-theme__glow-bright-color), transparent 90%) !important;
    }
    :deep(.data-list__row:hover::after) {
        --data-list__hover-background: color-mix(in srgb, var(--holo-theme__glow-bright-color), transparent 90%);
    }

    /***** AppChip *****/

    /* Variables */
    :deep(.app-chip) {
        /* Colors */
        --app-chip__chip-color-background-on:  var(--holo-theme__background-color-transparency-low) !important;
        --app-chip__chip-color-background-off: var(--holo-theme__background-color-off-transparency-low) !important;

        --app-chip__chip-color-text-off: color-mix(in srgb, white, transparent 55%) !important;
        --app-chip__chip-color-icon-on:  color-mix(in srgb, white, transparent 20%) !important;
        --app-chip__chip-color-icon-off: color-mix(in srgb, white, transparent 70%) !important;

        /* Glow */
        --app-chip__glow-spread-on: 25px;
        --app-chip__glow-spread-off: 10px;

        /* Overlay */
        --app-chip__overlay-hover: color-mix(in srgb, white, transparent 90%) !important;
    }
    :deep(.app-chip:hover) {
        /* Overlay color */
        --app-chip__overlay-color: var(--app-chip__overlay-hover);
    }
    :deep(.app-chip:active) {
        /* Overlay color */
        --app-chip__overlay-color: var(--app-chip__overlay-click);
    }

    /* Add glow effect */
    :deep(.app-chip.on) {
        box-shadow: 0 0 var(--app-chip__glow-spread-on) var(--app-chip__chip-color-background-on);
    }
    :deep(.app-chip.off) {
        box-shadow: 0 0 var(--app-chip__glow-spread-off) var(--app-chip__chip-color-background-off);
    }
    /* Add glow effect to overlay */
    :deep(.app-chip.on::after) {
        box-shadow: 0 0 var(--app-chip__glow-spread-on) var(--app-chip__overlay-color);
    }
    :deep(.app-chip.off::after) {
        box-shadow: 0 0 var(--app-chip__glow-spread-off) var(--app-chip__overlay-color);
    }

    /* On hover */
    :deep(.app-chip:hover) {
        /* Glow */
        --app-chip__glow-spread-on: 30px;
        --app-chip__glow-spread-off: 15px;
    }

    /* On click (start to transition to the other state) */
    :deep(.app-chip.on:active) {
        /* Color */
        --app-chip__overlay-click: color-mix(in srgb, var(--app-chip__overlay-hover), var(--app-chip__chip-color-background-off) 30%);
    }
    :deep(.app-chip.off:active) {
        /* Color */
        --app-chip__overlay-click: color-mix(in srgb, var(--app-chip__overlay-hover), var(--app-chip__chip-color-background-on) 10%);
    }
    :deep(.app-chip:active) {
        /* Glow */
        --app-chip__glow-spread-on: 25px;
        --app-chip__glow-spread-off: 20px;
    }

    /****************
    | Custom themes |
    ****************/

    /***** Pokeball *****/

    .holo-theme__theme-pokeball {
        /* Theme specific variables */
        --holo-theme__pokeball-red:   red;
        --holo-theme__pokeball-white: white;
        --holo-theme__pokeball-black: black;

        --holo-theme__pokeball-background-fade: 5%;
        --holo-theme__pokeball-background-red:   color-mix(in srgb, var(--holo-theme__app-background-base), var(--holo-theme__pokeball-red)   var(--holo-theme__pokeball-background-fade));
        --holo-theme__pokeball-background-white: color-mix(in srgb, var(--holo-theme__app-background-base), var(--holo-theme__pokeball-white) var(--holo-theme__pokeball-background-fade));
        --holo-theme__pokeball-background-black: color-mix(in srgb, var(--holo-theme__app-background-base), var(--holo-theme__pokeball-black) var(--holo-theme__pokeball-background-fade));

        /* App background */
        --holo-theme__app-background-base: hsl(0, 0%, 5%);
        --holo-theme__app-background-effect-color: hsla(340, 100%, 65%, 0.13);
        --holo-theme__app-background-effect: radial-gradient(
                                                 circle,
                                                 transparent                                16%,
                                                 var(--holo-theme__app-background-base) 18%
                                             ),
                                             radial-gradient(
                                                 circle,
                                                 var(--holo-theme__pokeball-background-white)      4.5%,
                                                 var(--holo-theme__pokeball-background-black) 5.5% 6.5%,
                                                 transparent                                  7.5%
                                             ),
                                             linear-gradient(
                                                 to bottom,
                                                 var(--holo-theme__pokeball-background-red)          48.75%,
                                                 var(--holo-theme__pokeball-background-black) 49.75% 50.25%,
                                                 var(--holo-theme__pokeball-background-white) 51.25%
                                             );
        --holo-theme__app-background-effect-size: 280px;

        /* Background colors */
        --container-background-filled: hsl(355, 70%, 50%);

        /* Pokeball background */
        --holo-theme__background: radial-gradient(
                                  circle,
                                      white  0% 18%,
                                      black 22% 28%,
                                      transparent 32%
                                  ),
                                  linear-gradient(
                                      to bottom,
                                      red    0%  43%,
                                      black 47%  53%,
                                      white 57% 100%
                                  );
        --holo-theme__background-opacity-low: 0.15;

        /* Glow colors */
        --holo-theme__glow-bright-color: rgb(255, 255, 255);
        --holo-theme__glow-medium-color: hsl(0, 100%, 75%);
    }

    .holo-theme__theme-pokeball.holo-theme__option-simplified,
    .holo-theme__theme-pokeball .holo-theme__option-simplified {
        /* Simplified background */
        --holo-theme__background: var(--holo-theme__background-color-transparency-high);
        --holo-theme__background-opacity-low: 1;
    }

    :deep(.holo-theme__theme-pokeball .v-application) {
        /* Background animation speed */
        --holo-theme__app-background-animation-speed: 2;
    }
</style>