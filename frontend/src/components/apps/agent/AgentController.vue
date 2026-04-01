<script setup>
    import { ref } from 'vue';
    import { startGame } from '@/services/agent';

    const opponent = ref('');

    /**
     * Sends a request to the API to start a new game against the specified opponent.
     */
    function challenge() {
        // Validate input
        if (!opponent.value) {
            throw new Error("Opponent username is required to start a game.");
        }

        // Send the request to the API
        startGame(opponent.value)
            .then(response => {
                console.log("Game started successfully:", response.data);
            })
            .catch(error => {
                console.error("Error starting game:", error);
            });
    }
</script>

<template>
    <HoloApp
        title="Challenge Pokestral !"
        :outputs="0"
    >

        <template #input>
            <HoloTextField
                label="Username"
                placeholder="Your Pokemon Showdown username here."

                v-model="opponent"
            />

            <HoloButton
                class="mt-8 w-50"
                @click="challenge()"
            > Challenge ! </HoloButton>
        </template>
    </HoloApp>
</template>

<style scoped>
</style>