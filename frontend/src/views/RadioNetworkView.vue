<script setup>
	import { ref } from 'vue';

	const visibility = ref({})
</script>

<template>
	<HoloTheme>
		<AppList
			v-model="visibility"
			:apps="[
				{ title: 'LTE Throughput Calculator', value: 'throughput-calculator', default: false},
				{ title: 'Sensor Link Simulator',     value: 'sensor-link-simulator', default: false},
				{ title: '5G Settings',               value: 'new-radio-settings',    default: true},
			]"
		>
			<ThroughputCalculator :show="visibility['throughput-calculator'] ?? false" />
			<SensorLinkSimulator :show="visibility['sensor-link-simulator'] ?? false" />
			<NewRadioSettings :show="visibility['new-radio-settings'] ?? false" />
		</AppList>
	</HoloTheme>
</template>