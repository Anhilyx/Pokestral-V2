<script setup>
	import { ref } from 'vue';

	const visibility = ref({})
</script>

<template>
	<HoloTheme theme="pokeball">
		<AppList
			v-model="visibility"
			:apps="[
				{ title: 'Damage Calculator', value: 'damage-calculator', default: true  },
				{ title: 'Dictionnary',       value: 'dictionnary',       default: false },
			]"
		>
			<DamageCalculator :show="visibility['damage-calculator'] ?? false" />
			<PokeDictionnary :show="visibility['dictionnary'] ?? false" />
		</AppList>
	</HoloTheme>
</template>