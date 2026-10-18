<script lang="ts">
	import TerritorySelect from '$lib/components/caudal/TerritorySelect.svelte';
	const {
		selectedCity = null,
		cityId,
		onChangeCity,
		class: className = ''
	}: {
		selectedCity?: { id: number; name: string; country: string } | null;
		cityId?: number;
		onChangeCity: (city: { id: number; name: string; country: string } | null) => void;
		class?: string;
	} = $props();
</script>

<div class={className}>
	<TerritorySelect
		selectedId={cityId ?? selectedCity?.id}
		onSelect={(city) =>
			onChangeCity(city?.id ? { id: city.id, name: city.name, country: city.country } : null)}
	/>
</div>
