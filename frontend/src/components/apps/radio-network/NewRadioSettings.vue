<script setup>
    import HoloStreetMapPlus from '@/components/apps/radio-network/components/HoloStreetMapPlus.vue';
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
            <HoloStreetMapPlus
                @area-changed=""
            />
        </template>

        <template #output-1>
        </template>

        <template #output-2>
        </template>
    </HoloApp>
</template>

<style scoped>
</style>