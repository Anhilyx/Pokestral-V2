<script setup>
	import { ref } from 'vue';

	const visibility = ref({})
</script>

<template>
	<HoloTheme theme="pokeball">
		<AppList
			v-model="visibility"
			:apps="[
				{ title: 'Damage Calculator', value: 'damage-calculator', default: true }
			]"
		>
			<DamageCalculator :show="visibility['damage-calculator'] ?? false" />
		</AppList>
	</HoloTheme>
</template>