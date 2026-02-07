<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue';

    const model = defineModel({});

    // Variables for CSS variable observation
    const el = ref(null);
    const cssVariables = ref({});
    let observer = null;

    // Retrieve CSS variables
    function fetchVariables() {
        if (!el.value) return {};

        const variables = {};
        if (el.value && el.value.computedStyleMap) {

            // Get computed style map
            const styleMap = el.value.computedStyleMap();
            for (const [prop, val] of styleMap) {

                // Retrieve only CSS variables (exclude Vuetify variables)
                if (prop.startsWith('--') && !prop.startsWith('--v-') && !variables[prop]) {
                    variables[prop] = val.toString();
                }
            }
        }

        return variables;
    };

    // Update CSS variables on mount
    onMounted(() => {
        cssVariables.value = fetchVariables();

        // Observe changes to classes and styles
        const target = el.value?.$el || el.value;
        if (target) {

            // Recompute variables on mutation
            observer = new MutationObserver(() => {
                cssVariables.value = fetchVariables();
            });

            // Watch for class and style changes
            observer.observe(target, {
                attributes: true,
                attributeFilter: ['class', 'style'],
                subtree: false
            });
        }
    });

    // Disconnect observer on unmount
    onBeforeUnmount(() => {
        if (observer) {
            observer.disconnect();
            observer = null;
        }
    });
   
    defineOptions({
        inheritAttrs: false
    });
</script>

<template>
    <HoloInput class="holo-select">
        <VSelect
            v-bind="$attrs"
            v-model="model"
            ref="el"

            variant="outlined"
            density="comfortable"
            :hide-details="true"
            menu-icon
           
            :menu-props="{
                style: cssVariables,
                contentClass: 'holo-select__menu'
            }"
        >
            <template #append-inner>
                <Icon icon="keyboard_arrow_down" :size="32" />
            </template>
        </VSelect>
    </HoloInput>
</template>

<style scoped>
    /* Variables */
    .holo-select {
        /* Layout */
        --holo-select__icon-glow: 0 0 var(--holo-theme__glow-strength-text-medium) var(--holo-theme__text-color-base);
    }

    .holo-select {
        /* Compensate for label */
        padding-top: calc(var(--holo-input__label-height) / 2);

        /* Blur background */
        backdrop-filter: blur(var(--holo-theme__blur-strength-medium)) !important;
        -webkit-backdrop-filter: blur(var(--holo-theme__blur-strength-medium)) !important;
    }

    .v-select {
        /* Background */
        background: var(--holo-input__background-color) !important;

        /* Glow effect */
        box-shadow: var(--holo-input__glow) !important;
    }

    /* On hover */
    .v-select:hover {
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

    .icon {
        /* Animation */
        text-shadow: 0 0 0px var(--holo-theme__text-color-base);
        transition: text-shadow var(--animation-speed-fast);
    }

    .v-select:hover .icon {
        /* Hover glow */
        text-shadow: var(--holo-select__icon-glow);
    }
</style>

<style>
    /* Variables */
    .holo-select__menu {
        /* Layout */
        --holo-select__menu-gap: 3px;

        /* Rendering */
        --holo-select__menu-rounded: 4px;
    }

    .holo-select__menu .v-list {
        /* Layout */
        display: flex !important;
        flex-direction: column !important;
        margin: 0 !important;
        padding: 0 !important;
        gap: var(--holo-select__menu-gap) !important;
       
        /* Background */
        background: none !important;
        backdrop-filter: blur(var(--holo-theme__blur-strength-high)) !important;
        -webkit-backdrop-filter: blur(var(--holo-theme__blur-strength-high)) !important;

        /* Hide scrollbar */
        scrollbar-width: none;
        -ms-overflow-style: none;
    }
    /* Hide scrollbar */
    .holo-select__menu .v-list::-webkit-scrollbar {
        display: none;
    }

    .holo-select__menu .v-list-item {
        /* Text */
        color: var(--holo-theme__text-color-muted) !important;

        /* Background */
        background: var(--holo-theme__background-color-transparency-medium) !important;

        /* Borders */
        border: 1px solid var(--holo-theme__glow-medium-weak) !important;
        border-radius: var(--holo-select__menu-rounded) !important;
    }

    /* On hover */
    .holo-select__menu .v-list-item:hover {
        /* Text */
        color: var(--holo-theme__text-color-base) !important;

        /* Glow effect */
        box-shadow: var(--holo-input__glow-hover) !important;
        text-shadow: var(--holo-input__glow-hover) !important;
    }
    .holo-select__menu .v-list-item:hover .v-list-item__overlay {
        /* Adjust overlay opacity on hover */
        background: var(--holo-theme__glow-bright-color) !important;
        opacity: 0.1 !important;
    }

    /* On active */
    .holo-select__menu .v-list-item--active {
        /* Text */
        color: var(--holo-theme__text-color-accentued) !important;

        /* Glow effect */
        border: 1px solid var(--holo-theme__glow-medium-strong) !important;
        box-shadow: var(--holo-input__glow-focus) !important;
        text-shadow: var(--holo-input__glow-focus) !important;

        /* Disable click */
        pointer-events: none !important;
    }
    .holo-select__menu .v-list-item--active * {
        /* Text */
        font-weight: bold !important;
    }
    .holo-select__menu .v-list-item--active .v-list-item__overlay {
        background: var(--holo-theme__glow-medium-color) !important;
        opacity: 0.3 !important;
    }
</style>