<script setup>
	import { ref } from 'vue';

	const visibility = ref({})
</script>

<template>
	<HoloTheme theme="pokeball">
		<AppList
			v-model="visibility"
			:apps="[
				{ title: 'Start Game',   value: 'startgame',  default: true  },
			]"
		>
			<AgentController :show="visibility['startgame'] ?? false" />
		</AppList>
	</HoloTheme>
</template>