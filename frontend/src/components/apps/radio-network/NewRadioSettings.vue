<script setup>
</script>

<template>
    <HoloApp
        title="5G Settings"
        :status="{
            output: true,
        }"
        :outputs="2"
    >

        <template #input>
            <HoloStreetMap />
        </template>

        <template #output-1>
        </template>

        <template #output-2>
        </template>
    </HoloApp>
</template>

<style scoped>
</style>