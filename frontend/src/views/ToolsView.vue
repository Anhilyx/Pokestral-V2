<script setup>
	import { ref } from 'vue';

	const visibility = ref({})
</script>

<template>
	<HoloTheme theme="pokeball">
		<AppList
			v-model="visibility"
			:apps="[
				{ title: 'Damage Calculator', value: 'damage-calculator', default: false },
				{ title: 'Dictionnary',       value: 'dictionnary',       default: false },
				{ title: 'Types Table',      value: 'types-table',        default: true  },
			]"
		>
			<DamageCalculator :show="visibility['damage-calculator'] ?? false" />
			<PokeDictionnary :show="visibility['dictionnary'] ?? false" />
			<TypesTable :show="visibility['types-table'] ?? false" />
		</AppList>
	</HoloTheme>
</template>