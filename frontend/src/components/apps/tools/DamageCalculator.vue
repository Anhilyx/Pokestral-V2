<script setup>
    import { ref } from 'vue';
    import { calculateDamage_knownAttacker, calculateDamage_knownDefender, calculateDamage_knownBoth, calculateDamage_knownNone } from '@/services/tools';

    const isAttackerKnown = ref(true);
    const attackerSet = ref(
        'Arceus @ Life Orb'               + '\n' +
        'Ability: Multitype'              + '\n' +
        'EVs: 228 Atk / 28 SpA / 252 Spe' + '\n' +
        'Naughty Nature'                  + '\n' +
        '- Swords Dance'                  + '\n' +
        '- Extreme Speed'                 + '\n' +
        '- Earthquake'                    + '\n' +
        '- Ice Beam'
    );
    const attackerName = ref('Arceus');
    const attackerMoves = ref('Swords Dance, Extreme Speed, Earthquake, Ice Beam');

    const isDefenderKnown = ref(false);
    const defenderSet = ref(
        'Blissey @ Leftovers'           + '\n' +
        'Ability: Natural Cure'         + '\n' +
        'EVs: 252 HP / 252 Def / 4 SpD' + '\n' +
        'Bold Nature'                   + '\n' +
        '- Seismic Toss'                + '\n' +
        '- Toxic'                       + '\n' +
        '- Soft-Boiled'                 + '\n' +
        '- Heal Bell'
    );
    const defenderName = ref('Blissey');

    const generation = ref(9);

    const result = ref(undefined);
    const error = ref(undefined);

    async function calculate() {
        try {
            let res;
           
            // Attacker set is known & defender set is unknown
            if (isAttackerKnown.value && !isDefenderKnown.value)
                res = await calculateDamage_knownAttacker({
                    attacker: attackerSet.value,
                    defender: defenderName.value,
                    generation: generation.value,
                });

            // Attacker set is unknown & defender set is known
            else if (!isAttackerKnown.value && isDefenderKnown.value)
                res = await calculateDamage_knownDefender({
                    attacker: attackerName.value,
                    defender: defenderSet.value,
                    moves: attackerMoves.value.split(',').map(move => move.trim()),
                    generation: generation.value,
                });

            // Attacker set is known & defender set is known
            else if (isAttackerKnown.value && isDefenderKnown.value)
                res = await calculateDamage_knownBoth({
                    attacker: attackerSet.value,
                    defender: defenderSet.value,
                    generation: generation.value,
                });

            // Attacker set is unknown & defender set is unknown
            else if (!isAttackerKnown.value && !isDefenderKnown.value)
                res = await calculateDamage_knownNone({
                    attacker: attackerName.value,
                    defender: defenderName.value,
                    moves: attackerMoves.value.split(',').map(move => move.trim()),
                    generation: generation.value,
                });
       
            // Store results
            result.value = res.data;
            error.value = undefined;
            console.log(res.data);
        }
       
        // Error case
        catch (err) {
            console.error(err);
            result.value = undefined;
            error.value = err;
        }
    }

    // Smooth scrolling + slowdown
    function scrollOverride(event, multiplier = 1) {
        // Define constants
        const SCROLL_DURATION = 200; // in ms
        const FPS = 60;

        // Retrive the data
        const element = event.currentTarget;
        const scroll = event.deltaY * multiplier;

        // Compute animation values
        let frame = 0;
        const totalFrames = (SCROLL_DURATION / 1000) * FPS;
        const scrollPerFrame = scroll / totalFrames;

        // Apply smooth scrolling effect
        const scrollInterval = setInterval(() => {
            element.scrollTop += scrollPerFrame;

            // Stop when done
            if (
                frame++ >= totalFrames ||
                (element.scrollTop === 0 && scrollPerFrame < 0) ||
                (element.scrollTop + element.clientHeight >= element.scrollHeight && scrollPerFrame > 0)
            ) {
                clearInterval(scrollInterval);
            }
        }, 1000 / FPS);
    }
</script>

<template>
    <HoloApp
        title="Damage Calculator"
        :outputs="2"
    >

        <template #input>
            <!-- Attacking Pokemon -->
            <HoloSwitch v-model="isAttackerKnown">
                Use full attacker set
            </HoloSwitch>
            <HoloTextArea v-if="isAttackerKnown"
                class="monospace"
                label="Attacker Set"
                :placeholder="
                    'Arceus @ Life Orb'               + '\n' +
                    'Ability: Multitype'              + '\n' +
                    'EVs: 228 Atk / 28 SpA / 252 Spe' + '\n' +
                    'Naughty Nature'                  + '\n' +
                    '- Swords Dance'                  + '\n' +
                    '- Extreme Speed'                 + '\n' +
                    '- Earthquake'                    + '\n' +
                    '- Ice Beam'
                "

                v-model="attackerSet"
                @blur="calculate()"
            />
            <div v-else>
                <HoloTextField
                    label="Attacker Name"
                    placeholder="Arceus"

                    v-model="attackerName"
                    @blur="calculate()"
                />
                <HoloTextField
                    class="monospace"
                    label="Attacker Moves"
                    placeholder="Swords Dance, Extreme Speed, Earthquake, Ice Beam"

                    v-model="attackerMoves"
                    @blur="calculate()"
                />
            </div>

            <!-- Defending Pokemon -->
            <HoloSwitch v-model="isDefenderKnown">
                Use full defender set
            </HoloSwitch>
            <HoloTextArea v-if="isDefenderKnown"
                class="monospace"
                label="Defender Set"
                :placeholder="
                    'Blissey @ Leftovers' + '\n' +
                    'Ability: Natural Cure' + '\n' +
                    'EVs: 252 HP / 252 Def / 4 SpD' + '\n' +
                    'Bold Nature' + '\n' +
                    '- Seismic Toss' + '\n' +
                    '- Toxic' + '\n' +
                    '- Soft-Boiled' + '\n' +
                    '- Heal Bell'
                "

                v-model="defenderSet"
                @blur="calculate()"
            />
            <HoloTextField v-else
                label="Defender Name"
                placeholder="Blissey"

                v-model="defenderName"
                @blur="calculate()"
            />

            <!-- Generation Selector -->
            <HoloSelect
                label="Generation"

                v-model="generation"
                @update:model-value="calculate()"
                :items="[
                    { title: 'Generation 1 (Red/Blue)',       value: 1 },
                    { title: 'Generation 2 (Gold/Silver)',    value: 2 },
                    { title: 'Generation 3 (Ruby/Sapphire)',  value: 3 },
                    { title: 'Generation 4 (Diamond/Pearl)',  value: 4 },
                    { title: 'Generation 5 (Black/White)',    value: 5 },
                    { title: 'Generation 6 (X/Y)',            value: 6 },
                    { title: 'Generation 7 (Sun/Moon)',       value: 7 },
                    { title: 'Generation 8 (Sword/Shield)',   value: 8 },
                    { title: 'Generation 9 (Scarlet/Violet)', value: 9 },
                ]"
            />
        </template>

        <template #output-1>
            <!-- Show loading if no result -->
            <div
                v-if="!(result ?? false)"
                class="d-flex justify-center align-center flex-grow-1"
            >
                <!-- Progress differs between with and without error -->
                <VProgressCircular
                    :class="{
                        'glitch': error ?? false
                    }"
                    color="var(--holo-theme__background-color)"
                    size="64" width="6"
                    indeterminate
                />
            </div>

            <!-- Else show result -->
            <div v-if="result ?? false">
                <div v-for="moveName in Object.keys(result.default)"
                    :key="moveName"
                    :class="{
                        'mt-4': moveName !== Object.keys(result.default)[0]
                    }"
                >
                    <h2> {{ moveName }} </h2>
                    <div
                        class="scrollable no-scrollbar"
                        style="max-height: 110px;"
                        @wheel.prevent="scrollOverride($event, 1/3)"
                    >
                        <DataList
                            class="py-0"
                            :items="Object.entries(result).map(([scenario, outcome]) => ({
                                title: scenario,
                                value: `${outcome[moveName].min} - ${outcome[moveName].max}`,
                            }))"
                        />
                    </div>
                </div>
            </div>
        </template>

        <template #output-2>
            <!-- Show loading if nothing -->
            <div
                v-if="!(result ?? false) && !(error ?? false)"
                class="d-flex justify-center"
            >
                <VProgressCircular
                    color="var(--holo-theme__background-color)"
                    size="64" width="6"
                    indeterminate
                />
            </div>

            <!-- Else show error/result -->
            <div v-else class="damage-calculator__output-json">
                <HoloTextArea
                    class="monospace"
                    :label="result ? 'Result JSON' : 'Error Message'"
                    :model-value="JSON.stringify(result ?? error, null, 1)"
                    readonly
                />
            </div>
        </template>
    </HoloApp>
</template>

<style scoped>
    /* Disable glitch effect on the title */
    :deep(.holo-app__title-container .glitch) {
        --glitch-strength-animation: 0deg;
    }

    /* Use a monospace font for the attacker set & JSON output */
    :deep(.monospace textarea),
    :deep(.monospace input) {
        font-family: 'Courier New', Courier, monospace;
    }

    /* Force output-2 textarea to take full height */
    /* (In a very beautifyl and elegant way ;) ) */
    .damage-calculator__output-json,
    .damage-calculator__output-json > *,
    .damage-calculator__output-json > * > *,
    .damage-calculator__output-json > * > * > *,
    .damage-calculator__output-json > * > * > * > * {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }

    /* Increase glitch effect on error */
    :deep(.v-progress-circular.glitch) {
        --glitch-strength-animation: 30deg;
        --glitch-strength-low:  1px;
        --glitch-strength-high: 5px;
    }

    :deep(.v-progress-circular.glitch .v-progress-circular__overlay),
    :deep(.v-progress-circular.glitch svg) {
        /* Change the speed of the animation */
        animation-duration: 0s !important;
    }
</style>