<script setup>
    import { ref } from 'vue';
    import {
        createFighter, createWaiter,
        getTeams, getAvailableMoves, getAvailableSwitches,
        sendAction
    } from '@/services/poke-env';
import HoloSwitch from '@/components/elements/holographic/HoloSwitch.vue';
import HoloSelect from '@/components/elements/holographic/HoloSelect.vue';
import HoloButton from '@/components/elements/holographic/HoloButton.vue';

    const props = defineProps({
        type: {
            type: String,
            required: true,
            validator: value => ['waiter', 'fighter'].includes(value)
        },

        placeholders: {
            type: Object,
            required: false,
            default: () => ({})
        }
    });

    const result = ref(null);
    const error = ref(null);

    const uuid = ref(null);

    const username = ref(props.placeholders?.username ?? '');
    const password = ref(props.placeholders?.password ?? '');
    const opponent = ref(props.placeholders?.opponent ?? '');

    const teams = ref(null);
    const availableMoves = ref(null);
    const availableSwitches = ref(null);

    const useMove = ref(true);

    const selectedMove = ref(null);
    const useMegaEvolution = ref(false);
    const useZMove = ref(false);
    const useDynamax = ref(false);
    const useTeracrystallization = ref(false);
    const selectedSwitch = ref(null);

    /**
     * Connects to the API to create a new fighter/waiter with the given credentials and opponent.
     */
    function connect() {
        // Format the body
        const body = {
            username: username.value,
            password: password.value,
            opponent: opponent.value === '' ? null : opponent.value,
        };

        // Send the request to the API
        if (props.type === 'waiter') {
            createWaiter(body)
                .then(response => {
                    uuid.value = response.data.uuid;
                    error.value = null;
                    updateBattle();
                })
                .catch(err => {
                    console.error('Error creating waiter:', err);
                    error.value = err.message;
                });
        } else {
            createFighter(body)
                .then(response => {
                    uuid.value = response.data.uuid;
                    error.value = null;
                    updateBattle();
                })
                .catch(err => {
                    console.error('Error creating fighter:', err);
                    error.value = err.message;
                });
        }
    }

    /**
     * Regularly fetch the current state of the battle from the API.
     */
    async function updateBattle() {
        if (uuid.value) {
            try {
                const [teamsResponse, movesResponse, switchesResponse] = await Promise.all([
                    getTeams(uuid.value),
                    getAvailableMoves(uuid.value),
                    getAvailableSwitches(uuid.value)
                ]);

                teams.value = teamsResponse.data;
                availableMoves.value = movesResponse.data;
                availableSwitches.value = switchesResponse.data;

                result.value = teams.value;
                error.value = null;
            } catch (err) {
                console.error('Error fetching battle state:', err);
                result.value = null;
                error.value = err.message;
            }
        }

        // Schedule the next update
        setTimeout(updateBattle, 1000);
    }

    /**
     * Sends the selected action to the API.
     */
    function act() {
        // Format the body
        let body = {}
        if (useMove.value) {
            body = {
                type: 'move',
                details: {
                    move: selectedMove.value,
                    use_mega_evolution: useMegaEvolution.value,
                    use_z_move: useZMove.value,
                    use_dynamax: useDynamax.value,
                    use_terastallization: useTeracrystallization.value,
                }
            };
        } else {
            body = {
                type: 'switch',
                details: {
                    pokemon: selectedSwitch.value
                }
            };
        }

        // Send the request to the API
        sendAction(uuid.value, body)
            .then(response => {
                error.value = null;
                updateBattle();
            })
            .catch(err => {
                console.error('Error sending action:', err);
                error.value = err.message;
            });
    }
</script>

<template>
    <HoloApp
        :title="props.type === 'waiter' ? 'Champion' : 'Challenger'"
        :outputs="2"
    >

        <template #input>
            <!-- If the fight hasn't started yet -->
            <div v-if="(!uuid || false)">
                <HoloTextField
                    label="Username"
                    :placeholder="props.placeholders?.username ?? 'Pokestral1'"

                    v-model="username"
                />
                <HoloTextField
                    label="Password"
                    placeholder="SuperSecretPassword"
                    type="password"

                    v-model="password"
                />

                <hr class="mt-4 mb-2" />

                <HoloTextField
                    label="Opponent"
                    :placeholder="props.placeholders?.opponent ?? 'Pokestral2'"

                    v-model="opponent"
                />

                <HoloButton
                    class="mt-8 w-50"
                    @click="connect()"
                > Connect </HoloButton>
            </div>

            <!-- If the fight is ongoing -->
            <div v-else>
                <!-- Select between using a move and switching out -->
                <div class="d-flex align-center justify-center">
                    <h3
                        class="mr-4"
                        :style="{ opacity: useMove ? 0.5 : 1 }"
                    > Switch </h3>
                    <HoloSwitch
                        v-model="useMove"
                    />
                    <h3
                        class="ml-1"
                        :style="{ opacity: useMove ? 1 : 0.5 }"
                    > Move </h3>
                </div>

                <hr class="mb-4 mt-2" />

                <!-- If using a move -->
                <div v-if="useMove" class="w-100">
                    <HoloSelect
                        class="w-100"
                        label="Selected Move"

                        v-model="selectedMove"
                        :items="
                            availableMoves?.map(move => ({
                                title: move.name,
                                value: move.name
                            })) ?? []
                        "
                    />

                    <VContainer>
                        <VRow>
                            <VCol class="pa-0">
                                <HoloSwitch
                                    v-model="useMegaEvolution"
                                > Mega Evolution </HoloSwitch>
                            </VCol>
                            <VCol class="pa-0">
                                <HoloSwitch
                                    v-model="useZMove"
                                > Z-Move </HoloSwitch>
                            </VCol>
                        </VRow>
                        <VRow>
                            <VCol class="pa-0">
                                <HoloSwitch
                                    v-model="useDynamax"
                                > Dynamax </HoloSwitch>
                            </VCol>
                            <VCol class="pa-0">
                                <HoloSwitch
                                    v-model="useTeracrystallization"
                                > Teracrystallization </HoloSwitch>
                            </VCol>
                        </VRow>
                    </VContainer>
                </div>

                <!-- If switching out -->
                <div v-else class="w-100">
                    <HoloSelect
                        class="w-100"
                        label="Selected Pokémon"

                        v-model="selectedSwitch"
                        :items="
                            availableSwitches?.map(switchOption => ({
                                title: switchOption.name,
                                value: switchOption.name
                            })) ?? []
                        "
                    />
                </div>

                <hr class="mb-6 mt-2" />

                <HoloButton
                    class="w-50"
                    @click="act()"
                > Go ! </HoloButton>
            </div>
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
            <div v-else>
                NOT IMPLEMENTED YET.
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
    /* Use a monospace font for the attacker set & JSON output */
    :deep(.monospace textarea),
    :deep(.monospace input) {
        font-family: 'Courier New', Courier, monospace;
    }
</style>