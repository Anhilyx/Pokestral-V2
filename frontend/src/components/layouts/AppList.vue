<script setup>
	import { onMounted } from 'vue';

	const visibility = defineModel({
		type: Object,
		required: true,
	});

	const props = defineProps({
		apps: {
			type: Array,
			required: true,
		},
	});

	// Open default app(s)
	onMounted(() => {
		for (const app of props.apps) {
			if (app.default)
				visibility.value[app.value] = true;
		}
	});
</script>

<template>
	<VApp class="app-list">
		<div class="app-list__chips no-scrollbar">
			<AppChip v-for="app in props.apps" :key="app.value"
				class="app-list__chip"
				style="--app_chip__height: var(--app-list__chips-height);"

				v-model="visibility[app.value]"
				:name="app.title"
			/>
		</div>

		<VMain class="no-scrollbar">
			<slot></slot>
		</VMain>
	</VApp>
</template>

<style scoped>
	/* Variables */
	.v-application {
		--app-list__chips-height: 40px;
		--app-list__chips-spacing: 20px;

		--app-list__spacing: 40px;
	}

	.v-application {
		/* Full viewport size */
		width: 100vw;
		height: 100vh;
		overflow: hidden;
	}

	.app-list__chips {
		/* Layout */
		display: flex;
		align-items: center;
		justify-content: left;
		padding: var(--app-list__chips-spacing);
		gap: var(--app-list__chips-spacing);
		overflow-x: scroll;
	}

	.app-list__chip {
		/* Size */
		height: var(--app-list__chips-height);
	}

	.v-main {
		/* Layout */
		display: flex;
		justify-content: center;
		height: calc(100vh - var(--app-list__chips-height) - var(--app-list__chips-spacing) * 2);
		overflow: auto;

		/* Spacing */
		padding: var(--app-list__spacing) 0;
		gap: var(--app-list__spacing);
	}
</style>