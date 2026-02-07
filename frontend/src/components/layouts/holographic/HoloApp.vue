<script setup>
    import HoloTheme from '@/components/themes/HoloTheme.vue';
import { watch } from 'vue';

    const props = defineProps({
        show: {
            type: Boolean,
            default: true
        },
        width: {
            type: Number,
            default: 700
        },

        title: {
            type: String,
            default: ""
        },
        outputs: {
            type: Number,
            default: 1
        },

        status: {
            type: Object,
            default: {}
        },
        
        sound: {
            type: Function,
            default: (audioCtx, isOpening) => {
                // Retrieve current time
                const t = audioCtx.currentTime;
                
                // Define duration based on open/close
                const duration = isOpening ? 0.2 : 0.13;
                
                // Create audio nodes
                const osc1 = audioCtx.createOscillator();
                const osc2 = audioCtx.createOscillator();
                const filter = audioCtx.createBiquadFilter();
                const masterGain = audioCtx.createGain();

                // Routing
                osc1.connect(filter);
                osc2.connect(filter);
                filter.connect(masterGain);
                masterGain.connect(audioCtx.destination);

                // Create sound envelope
                masterGain.gain.setValueAtTime(0, t);
                masterGain.gain.linearRampToValueAtTime(0.25, t + 0.01); 
                masterGain.gain.exponentialRampToValueAtTime(0.001, t + duration);

                // Oscillator settings
                osc1.type = 'sawtooth';
                osc2.type = 'square';
                osc1.detune.value = -10; 
                osc2.detune.value = 10;

                // Opening sound
                if (isOpening) {
                    osc1.frequency.setValueAtTime(200, t);
                    osc1.frequency.linearRampToValueAtTime(800, t + duration);
                    osc2.frequency.setValueAtTime(204, t);
                    osc2.frequency.linearRampToValueAtTime(804, t + duration);

                    filter.type = 'lowpass';
                    filter.frequency.setValueAtTime(100, t);
                    filter.frequency.exponentialRampToValueAtTime(12000, t + duration);
                    filter.Q.value = 8;
                }
                
                // Closing sound
                else {
                    osc1.frequency.setValueAtTime(500, t);
                    osc1.frequency.linearRampToValueAtTime(100, t + duration);
                    osc2.frequency.setValueAtTime(504, t);
                    osc2.frequency.linearRampToValueAtTime(104, t + duration);

                    filter.type = 'lowpass';
                    filter.frequency.setValueAtTime(5000, t);
                    filter.frequency.exponentialRampToValueAtTime(50, t + duration); 
                    filter.Q.value = 1;
                }

                // Start
                osc1.start(t);
                osc2.start(t);
                // Stop
                osc1.stop(t + duration + 0.05);
                osc2.stop(t + duration + 0.05);
                
                // Cleanup after sound ends
                setTimeout(() => {
                    masterGain.disconnect();
                }, (duration * 1000) + 100);
            }
        }
    });

    // Prepare audio context for toggle sounds
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    var audioCtx = new AudioContext();
    // Play a sound on toggle (different for open/close)
    watch(
        () => props.show,

        (isOpening) => {
            // Resume context if suspended (autoplay policy)
            if (audioCtx.state === 'suspended') audioCtx.resume();

            // Play sound
            props.sound(audioCtx, isOpening);
        }
    );
</script>

<template>
    <HoloTheme
        class="holo-app"
        :style="{
            width: `${props.show ? props.width : 0}px`,
            pointerEvents: props.show ? 'auto' : 'none'
        }"
    >
        <div
            class="holo-app__wrapper"
        >

        <!-- Title -->
        <HoloTheme class="holo-app__title-container" :options="['simplified']">
            <HoloDiv
                :show="show"
                :width="props.width - 180"
                class="glitch"
                :status="props.status.title"
            >
                <div class="holo-app__title-content nowrap" ref="titleDiv">
                    <h2> {{ title }} </h2>
                </div>
            </HoloDiv>
        </HoloTheme>

        <!-- Input -->
        <div
            class="holo-app__input-container"
        >
            <HoloDiv
                :show="show"
                :width="props.width - 60"
                :status="props.status.input"
            >
                <div class="holo-app__input-content" ref="inputDiv">
                    <slot name="input"></slot>
                </div>
            </HoloDiv>
        </div>

        <!-- Output(s) -->
        <HoloTheme
            class="holo-app__output-layout"
            :options="['simplified']"
        >
            <div v-for="index in props.outputs" :key="index"
                class="holo-app__output-container"
                :style="{
                    width: `${props.width / props.outputs}px`,
                }"
            >
                <HoloDiv
                    :show="show"
                    :width="props.width / props.outputs"
                    :status="props.status.output"
                >
                    <div class="h-100 d-flex">
                        <div class="holo-app__output-content">
                            <slot :name="`output-${index}`"></slot>
                        </div>
                    </div>
                </HoloDiv>
            </div>
        </HoloTheme>

        </div>
    </HoloTheme>
</template>

<style scoped>
    /* Variables */
    .holo-app {
        /* Boxes layout */
        --holo-app__title-offset: 20px;
        --holo-app__input-offset: -102px;
        --holo-app__output-offset: -95px;
        --holo-app__input-extra-up: 92px;
        --holo-app__input-extra-down: 85px;

        /* Inner layout */
        --holo-app__input-spacing: 20px;
        --holo-app__rounded-small: 12px;
        --holo-app__rounded-large: 16px;
        --holo-theme__blur-strength-low: 4px;
    }

    .holo-app {
        /* Animation */
        transition: width var(--animation-speed-medium);
    }

    .holo-app__wrapper {
        /* Layout */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: start;
        position: relative;

        /* Size */
        height: 0;
    }

    /***************
    | Title styles |
    ***************/

    .holo-app__title-container {
        /* Position */
        position: relative;
        top: var(--holo-app__title-offset);
        z-index: 3;

        /* Layout */
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .holo-app__title-content {

        /* Layout */
        display: flex;
        align-items: center;
        justify-content: center;

        /* Text style */
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    :deep(.holo-app__title-container .holo-div__background) {
        /* Background */
        backdrop-filter: blur(var(--holo-theme__blur-strength-low));
        -webkit-backdrop-filter: blur(var(--holo-theme__blur-strength-low));

        /* Shape */
        border-radius: var(--holo-app__rounded-small);
    }

    /***************
    | Input styles |
    ***************/

    .holo-app__input-container {
        /* Position */
        position: relative;
        top: calc(var(--holo-app__title-offset) + var(--holo-app__input-offset));
        z-index: 1;
    }

    .holo-app__input-content {
        /* Position */
        padding: calc(var(--holo-app__input-extra-up) +   var(--holo-app__input-spacing))
                                                          var(--holo-app__input-spacing)
                 calc(var(--holo-app__input-extra-down) + var(--holo-app__input-spacing))
                                                          var(--holo-app__input-spacing);

        /* Layout */
        display: flex;
        flex-direction: column;
        gap: var(--holo-app__input-spacing);
    }

    :deep(.holo-app__input-container .holo-div__background) {
        /* Shape */
        border-radius: var(--holo-app__rounded-large);
    }

    /* Blurred background for Pokeball theme */
    .holo-theme__theme-pokeball .holo-app__input-container :deep(.holo-div__background) {
        /* Stronger blur to hide background details */
        backdrop-filter: blur(calc(var(--holo-theme__blur-strength-low) * 1.5));
        -webkit-backdrop-filter: blur(calc(var(--holo-theme__blur-strength-low) * 1.5));
    }

    /****************
    | Output styles |
    ****************/

    .holo-app__output-layout {
        /* Position */
        position: relative;
        top: calc(var(--holo-app__title-offset) + var(--holo-app__input-offset) + var(--holo-app__output-offset));
        z-index: 2;

        /* Layout */
        display: flex;
    }

    .holo-app__output-container {
        /* Layout */
        display: flex;
        justify-content: center;
    }

    .holo-app__output-content {
        /* Layout */
        display: flex;
        flex-direction: column;
        padding: var(--holo-app__input-spacing);
        flex-grow: 1;
    }

    .holo-app__output-container .holo-div,
    :deep(.holo-app__output-container > * > .holo-theme) {
        /* Force the same height for all outputs */
        display: flex;
        height: 100%;
    }

    :deep(.holo-app__output-container .holo-div__background) {
        /* Background */
        backdrop-filter: blur(var(--holo-theme__blur-strength-low));
        -webkit-backdrop-filter: blur(var(--holo-theme__blur-strength-low));

        /* Shape */
        border-radius: var(--holo-app__rounded-large);
    }
</style>