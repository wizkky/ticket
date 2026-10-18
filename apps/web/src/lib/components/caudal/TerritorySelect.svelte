<script lang="ts">
	import { createQuery } from '@tanstack/svelte-query';
	import { caudalCities, type CitySchema } from '$lib/api';
	import * as m from '$lib/paraglide/messages.js';
	const uniqueId = $props.id();
	const {
		id = uniqueId,
		selectedId,
		onSelect,
		includeAll = true
	}: {
		id?: string;
		selectedId?: number | null;
		onSelect: (city: CitySchema | null) => void;
		includeAll?: boolean;
	} = $props();
	const cities = createQuery(() => ({
		queryKey: ['caudal-territory-cities'],
		queryFn: async () => {
			const result = await caudalCities();
			if (!result.data) throw new Error('Territory unavailable');
			return result.data;
		},
		staleTime: 300000
	}));
	function change(event: Event) {
		const value = (event.currentTarget as HTMLSelectElement).value;
		onSelect(cities.data?.find((city) => city.id === Number(value)) ?? null);
	}
</script>

<div class="space-y-2">
	<label for={id} class="block text-sm font-medium">{m['workspace.commune']()}</label>
	<select
		{id}
		class="min-h-11 w-full rounded-md border border-input bg-background px-3 text-sm"
		value={selectedId ?? ''}
		onchange={change}
		disabled={cities.isPending}
		aria-describedby="{id}-hint"
	>
		<option value="">{includeAll ? m['workspace.allCommunes']() : m['workspace.commune']()}</option>
		{#each cities.data ?? [] as city (city.id)}<option value={city.id ?? ''}>{city.name}</option
			>{/each}
	</select>
	<p id="{id}-hint" class="text-xs leading-relaxed text-muted-foreground">
		{m['workspace.communeHint']()}
	</p>
	{#if cities.isError}<p role="alert" class="text-xs text-destructive">
			{m['workspace.dataUnavailable']()}
			<button type="button" class="underline underline-offset-4" onclick={() => cities.refetch()}
				>{m['financials.retry']()}</button
			>
		</p>{/if}
</div>
