<script setup>
	import { ref } from 'vue';

	const visibility = ref({})
</script>

<template>
	<HoloTheme theme="pokeball">
		<AppList
			v-model="visibility"
			:apps="[
				{ title: 'Champion',   value: 'waiter',  default: true  },
				{ title: 'Challenger', value: 'fighter', default: true  },
			]"
		>
			<PokeEnv
				:show="visibility['waiter'] ?? false"
				type="waiter"
				:placeholders="{
					username: 'Pokestral1',
					password: 'password',
					opponent: 'Pokestral2'
				}"
			/>
			<PokeEnv
				:show="visibility['fighter'] ?? false"
				type="fighter"
				:placeholders="{
					username: 'Pokestral2',
					password: 'password',
					opponent: 'Pokestral1'
				}"
			/>
		</AppList>
	</HoloTheme>
</template>