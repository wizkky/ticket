<script lang="ts">
	import { SvelteURLSearchParams } from 'svelte/reactivity';
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { ArrowUpRight } from '@lucide/svelte';
	import { activityCategories } from '$lib/caudal/categories';
	import * as m from '$lib/paraglide/messages.js';
	interface Props {
		active?: string;
		compact?: boolean;
	}
	const { active, compact = false }: Props = $props();
	const categories = $derived(activityCategories());
	function categoryHref(id?: string) {
		const params = new SvelteURLSearchParams(page.url.searchParams);
		params.delete('page');
		params.delete('tags');
		if (id) params.set('category', id);
		else params.delete('category');
		return `${resolve('/(public)/events', {})}${params.size ? `?${params}` : ''}`;
	}
</script>

<nav class="categories" class:compact aria-label={m['creative.categoriesTitle']()}>
	{#if compact}
		<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- categoryHref resolves the route before preserving the current query -->
		<a href={categoryHref()} aria-current={!active ? 'page' : undefined}>
			{m['creative.allCategories']()}
		</a>
	{/if}
	{#each categories as category, i (category.id)}
		<!-- eslint-disable-next-line svelte/no-navigation-without-resolve -- categoryHref resolves the route before preserving the current query -->
		<a href={categoryHref(category.id)} aria-current={active === category.id ? 'page' : undefined}>
			{#if !compact}<span class="index" aria-hidden="true">0{i + 1}</span>{/if}
			<span>{category.label}</span><ArrowUpRight size={compact ? 14 : 18} aria-hidden="true" />
		</a>
	{/each}
</nav>

<style>
	.categories {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		border-top: 1px solid hsl(var(--border));
	}
	a {
		display: flex;
		align-items: center;
		gap: 18px;
		padding: 25px 16px 25px 0;
		border-bottom: 1px solid hsl(var(--border));
		font-size: 13px;
		min-height: 70px;
		transition: background 0.2s;
	}
	a:hover,
	a[aria-current] {
		background: hsl(var(--muted));
	}
	a > span:not(.index) {
		flex: 1;
	}
	.index {
		font-size: 10px;
		color: hsl(var(--muted-foreground));
		align-self: flex-start;
	}
	a :global(svg) {
		flex-shrink: 0;
	}
	.compact {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		border: 0;
	}
	.compact a {
		padding: 10px 14px;
		min-height: 44px;
		border: 1px solid hsl(var(--border));
		border-radius: 24px;
		font-size: 12px;
	}
	.compact a[aria-current] {
		background: hsl(var(--foreground));
		color: hsl(var(--background));
	}
	@media (max-width: 1023px) {
		.categories:not(.compact) {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
	}
	@media (max-width: 479px) {
		a {
			gap: 9px;
			padding-right: 10px;
			font-size: 12px;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		a {
			transition: none;
		}
	}
</style>
