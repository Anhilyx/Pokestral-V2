<script setup>
    import { ref, computed } from 'vue';

    const content = ref(null);

    const props = defineProps({
        show: {
            type: Boolean,
            default: true
        },
        width: {
            type: Number,
            default: null
        },

        status: {
            type: String,
            default: null,
            validator: (value) => [
                'error', 'warning', 'blink',
                null, undefined
            ].includes(value)
        }
    });

    const width = computed(() => {
        return props.width ?? content?.value?.offsetWidth ?? 0;
    });
</script>

<template>
    <!-- Wrapper handle smooth show/hide. -->
    <HoloTheme
        class="holo-div"
        :style="{
            pointerEvents: props.show ? 'auto' : 'none',
            '--holo-div__width': `${width}px`,
            '--holo-div__show': props.show ? 1 : 0,
        }"
    >
        <!-- Background handle smooth background animation. -->
        <div
            class="holo-div__background"
            :class="{
                'holo-div__notif-error': props.status === 'error',
                'holo-div__notif-warning': props.status === 'warning',
                'holo-div__notif-blink': props.status === 'blink',
            }"
        >
            <!-- Border allow proper overflow hiding -->
            <div
                class="holo-div__border"
            >
                <!-- Container handle content size. -->
                <div
                    ref="content"
                    class="holo-div__content"
                >
                    <slot></slot>
                </div>
            </div>
        </div>
    </HoloTheme>
</template>

<style scoped>
    /***** Explaination **************************************
    | - .holo-div: defines variables, hide the borders ;     |
    | - .holo-div__background: handle borders ;              |
    | - .holo-div__background::before: handles background ;  |
    | - .holo-div__background::after: handle notifications ; |
    | - .holo-div__border: handle proper inner show/hide ;   |
    | - .holo-div__content: contains the actual content.     |
    *********************************************************/

    /* Variables */
    .holo-div {
        /* Render */
        --holo-div__show: 1;
        --holo-div__width: 0px;

        /* Border */
        --holo-div__border-width: 20px;
        --holo-div__border-glow-weak-base:     calc(var(--holo-div__border-width) / 2 * 1.0);
        --holo-div__border-glow-weak-spread:   calc(var(--holo-div__border-width) / 2 * 0.2);
        --holo-div__border-glow-strong-base:   calc(var(--holo-div__border-width) / 2 * 0.5);
        --holo-div__border-glow-strong-spread: calc(var(--holo-div__border-width) / 2 * 0.1);
        --holo-div__border-glow-weak: var(--holo-div__border-glow-weak-base) var(--holo-div__border-glow-weak-spread);
        --holo-div__border-glow-strong: var(--holo-div__border-glow-strong-base) var(--holo-div__border-glow-strong-spread);

        /* Content */
        --holo-div__content-padding: 20px;

        /* Notifications colors */
        --holo-div__notif-background-color: transparent;
        --holo-div__notif-glow-color-weak:   var(--holo-theme__glow-bright-weak);
        --holo-div__notif-glow-color-strong: var(--holo-theme__glow-bright-strong);
        --holo-div__notif-glow-color-percent: 70%;
        /* Notifications glow */
        --holo-div__notif-glow-strength-multiplier: 1.0;
        /* Notification speed */
        --holo-div__notif-animation-speed: 3s;
    }
    .holo-div__background {
        /* Notifications glow */
        --holo-div__notif-glow-strength-weak:   calc(var(--holo-div__border-glow-weak-base)   * var(--holo-div__notif-glow-strength-multiplier)) calc(var(--holo-div__border-glow-weak-spread)   * var(--holo-div__notif-glow-strength-multiplier));
        --holo-div__notif-glow-strength-strong: calc(var(--holo-div__border-glow-strong-base) * var(--holo-div__notif-glow-strength-multiplier)) calc(var(--holo-div__border-glow-strong-spread) * var(--holo-div__notif-glow-strength-multiplier));
    }

    .holo-div,
    .holo-div__background,
    .holo-div__border {
        display: flex;
        overflow-x: hidden;

        /* Animation */
        transition: width var(--animation-speed-medium) ease-in-out,
                    margin var(--animation-speed-medium) ease-in-out;
    }

    .holo-div {
        /* Layout */
        width: calc(var(--holo-div__width) * var(--holo-div__show));
    }

    .holo-div__background {
        /* Layout */
        position: relative;
        width: calc((var(--holo-div__width) - var(--holo-div__border-width)) * var(--holo-div__show));
        margin: calc(var(--holo-div__border-width) / 2) calc(var(--holo-div__border-width) / 2 * var(--holo-div__show));
        
        /* Borders */
        box-shadow:       0 0 var(--holo-div__border-glow-weak)   var(--holo-theme__glow-bright-weak),
                          0 0 var(--holo-div__border-glow-strong) var(--holo-theme__glow-bright-strong),
                    inset 0 0 var(--holo-div__border-glow-weak)   var(--holo-theme__glow-bright-weak),
                    inset 0 0 var(--holo-div__border-glow-strong) var(--holo-theme__glow-bright-strong);

        /* Notifs */
        animation: blink-borders var(--holo-div__notif-animation-speed) infinite;
    }

    .holo-div__border {
        /* Layout */
        padding: calc(var(--holo-div__content-padding) / 2);
        justify-content: center;
        width: calc((var(--holo-div__width) - var(--holo-div__border-width)) * var(--holo-div__show));

        /* Smooth hiding */
        mask-image: linear-gradient(
            to right,
            transparent 0px,
            black 10px,
            black calc(100% - 10px),
            transparent 100%
        );
        -webkit-mask-image: linear-gradient(
            to right,
            transparent 0px,
            black 10px,
            black calc(100% - 10px),
            transparent 100%
        );
    }

    .holo-div__content {
        /* Layout */
        width: calc(var(--holo-div__width) - var(--holo-div__border-width) - var(--holo-div__content-padding));
        
        /* Force Size */
        flex-shrink: 0;
        flex-grow: 1;
    }

    /****************
    | Notifications |
    ****************/

    .holo-div__background::after {
        content: "";

        /* Position */
        position: absolute;
        inset: 0;
        z-index: 1;

        /* Notifs */
        animation: blink-background var(--holo-div__notif-animation-speed) infinite;

        /* Events */
        pointer-events: none;
    }
    
    /* Blink animations */
    @keyframes blink-background {
        0%, 30%, 70%, 100% {
            background: transparent
        }

        50% {
            background: var(--holo-div__notif-background-color);
        }
    }
    @keyframes blink-borders {
        0%, 30%, 70%, 100% {
            box-shadow:       0 0 var(--holo-div__border-glow-weak)   var(--holo-theme__glow-bright-weak),
                              0 0 var(--holo-div__border-glow-strong) var(--holo-theme__glow-bright-strong),
                        inset 0 0 var(--holo-div__border-glow-weak)   var(--holo-theme__glow-bright-weak),
                        inset 0 0 var(--holo-div__border-glow-strong) var(--holo-theme__glow-bright-strong);
        }

        50% {
            box-shadow:       0 0 var(--holo-div__notif-glow-strength-weak)   color-mix(in srgb, var(--holo-theme__glow-bright-weak),   var(--holo-div__notif-glow-color-weak)   var(--holo-div__notif-glow-color-percent)),
                              0 0 var(--holo-div__notif-glow-strength-strong) color-mix(in srgb, var(--holo-theme__glow-bright-strong), var(--holo-div__notif-glow-color-strong) var(--holo-div__notif-glow-color-percent)),
                        inset 0 0 var(--holo-div__notif-glow-strength-weak)   color-mix(in srgb, var(--holo-theme__glow-bright-weak),   var(--holo-div__notif-glow-color-weak)   var(--holo-div__notif-glow-color-percent)),
                        inset 0 0 var(--holo-div__notif-glow-strength-strong) color-mix(in srgb, var(--holo-theme__glow-bright-strong), var(--holo-div__notif-glow-color-strong) var(--holo-div__notif-glow-color-percent));
        }
    }

    /***** Error *****/
    
    .holo-div__background.holo-div__notif-error {
        /* Colors */
        --holo-div__notif-background-color:  hsla(350, 100%, 50%, 0.1);
        --holo-div__notif-glow-color-weak:   hsla(350, 100%, 60%, 0.4);
        --holo-div__notif-glow-color-strong: hsla(350, 100%, 60%, 1.0);

        /* Glow */
        --holo-div__notif-glow-strength-multiplier: 1.5;
    }

    /***** Warning *****/

    .holo-div__background.holo-div__notif-warning {
        /* Colors */
        --holo-div__notif-background-color:  hsla(20, 100%, 50%, 0.1);
        --holo-div__notif-glow-color-weak:   hsla(20, 100%, 50%, 0.4);
        --holo-div__notif-glow-color-strong: hsla(20, 100%, 50%, 1.0);

        /* Glow */
        --holo-div__notif-glow-strength-multiplier: 1.5;
    }

    /***** Blink *****/

    .holo-div__background.holo-div__notif-blink {
        /* Colors */
        --holo-div__notif-background-color:  hsla(210, 100%, 80%, 0.1);
        --holo-div__notif-glow-color-weak:   hsla(210, 100%, 80%, 0.4);
        --holo-div__notif-glow-color-strong: hsla(210, 100%, 80%, 1.0);

        /* Glow */
        --holo-div__notif-glow-strength-multiplier: 1.5;

        /* Faster animation */
        --holo-div__notif-animation-speed: 1.5s;
    }

    /****************
    | Custom themes |
    ****************/

    /* Allow custom background */
    .holo-div__background::before {
        content: "";

        /* Position */
        position: absolute;
        inset: 0;
        z-index: -1;

        /* Background */
        background: var(--holo-theme__background);
        opacity: var(--holo-theme__background-opacity-low);
    }
</style>