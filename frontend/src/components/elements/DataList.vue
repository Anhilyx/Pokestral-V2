<script setup>
    const props = defineProps({
        items: {
            type: Array,
            required: true
        }
    });
</script>

<template>
    <VContainer class="data-list">
        <div v-for="item in props.items"
            :key="item.title"
            class="data-list__row"
        >
            <div class="data-list__col nowrap weak"> {{ item.title }} </div>
            <div class="data-list__col nowrap strong"> {{ item.value }} </div>
        </div>
    </VContainer>
</template>

<style scoped>
    /* Variables */
    .data-list {
        --data-list__hover-background: rgba(255, 255, 255, 0.05);
    }

    .data-list__row {
        /* Layout */
        display: flex;
        flex-direction: row;
        align-items: end;
        position: relative;
    }

    .data-list__row:not(:last-child) {
        /* Separator line */
        border-bottom: solid 1px;
    }

    .data-list__row::after {
        content: '';

        /* Position */
        position: absolute;
        inset: 0;

        /* Animation */
        background: transparent;
        transition: background var(--animation-speed-fast) ease-in-out;
    }

    .data-list__row:hover::after {
        /* Hover effect */
        background: var(--data-list__hover-background);
    }

    .data-list__col {
        /* Layout */
        padding: 8px 6px;
    }

    /* Texts alignment */
    .data-list__col:first-child {
        flex-grow: 1;
    }
</style>