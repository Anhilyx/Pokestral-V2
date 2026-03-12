<script setup>
    defineProps({
        values: {
            type: Object,
            required: true
        },
        types: {
            type: Array,
            required: true
        },
        invert: {
            type: Boolean,
            default: false
        }
    })
</script>

<template>
    <table class="types-table">
        <thead>
            <tr>
                <th></th>
                <th v-for="defType in types"
                    :key="defType"
                >
                    {{ defType }}
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="attType in types"
                :key="attType"
            >
                <th> {{ attType }} </th>
                <td v-for="defType in types"
                    :key="defType"
                    :class="{
                        'x4': values[invert ? defType : attType]?.[invert ? attType : defType] === 4,
                        'x2': values[invert ? defType : attType]?.[invert ? attType : defType] === 2,
                        'x1': values[invert ? defType : attType]?.[invert ? attType : defType] === 1,
                        'x05': values[invert ? defType : attType]?.[invert ? attType : defType] === 0.5,
                        'x025': values[invert ? defType : attType]?.[invert ? attType : defType] === 0.25,
                        'x0': values[invert ? defType : attType]?.[invert ? attType : defType] === 0,
                        'x-1': values[invert ? defType : attType]?.[invert ? attType : defType] === undefined
                    }"
                >
                    {{ values[invert ? defType : attType]?.[invert ? attType : defType] !== undefined ? values[invert ? defType : attType][invert ? attType : defType] : '' }}
                </td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>
    .types-table {
        --types-table-size: 8px;
    }

    .types-table {
        font-size: var(--types-table-size);
        border-collapse: collapse;
        border: none;
    }

    .types-table thead th {
        writing-mode: vertical-rl;
    }

    .types-table th {
        text-align: left;
    }
    .types-table td {
        text-align: center;
        min-width: var(--types-table-size);
        min-height: var(--types-table-size);
        max-width: var(--types-table-size);
        max-height: var(--types-table-size);
        overflow: hidden;
    }

    .types-table .x4 {
        background-color: #800;
        color: #f66;
    }
    .types-table .x2 {
        background-color: #e22;
        color: #200;
    }
    .types-table .x1 {
        background-color: #fff4;
        color: #fff3;
    }
    .types-table .x05 {
        background-color: #2e2;
        color: #060;
    }
    .types-table .x025 {
        background-color: #080;
        color: #6f6;
    }
    .types-table .x0 {
        background-color: #888;
        color: #fff
    }
    .types-table .x-1 {
        background-color: #0004;
    }
</style>