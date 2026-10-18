<script lang="ts">
	// Keep the shared interface so the Caudal identity also reaches account surfaces.
	import { asset } from '$app/paths';
	import { cn } from '$lib/utils';
	interface Props {
		class?: string;
		mono?: boolean;
		mark?: boolean;
	}
	const { class: className = '', mono = false, mark = true }: Props = $props();
</script>

<span class={cn('caudal-wordmark text-2xl', mono && 'mono', className)}>
	{#if mark}
		<span class="symbol" aria-hidden="true"
			><img src={asset('/brand/caudal/symbol.png')} alt="" width="2048" height="2048" /></span
		>
	{/if}
	<span class="name"
		><!-- i18n-ignore: product name --><span>caudal</span><span class="suffix">Tickets</span></span
	>
</span>

<style>
	.caudal-wordmark {
		display: inline-flex;
		align-items: center;
		gap: 0.45em;
		white-space: nowrap;
		line-height: 1;
	}
	.name {
		display: flex;
		flex-direction: column;
		gap: 0.16em;
		font-family: 'Manrope', sans-serif;
		font-weight: 600;
		letter-spacing: -0.055em;
	}
	.suffix {
		font-family: 'DM Sans', sans-serif;
		font-size: 0.28em;
		letter-spacing: 0.35em;
		text-transform: uppercase;
		padding-left: 0.15em;
		font-weight: 500;
	}
	.symbol {
		position: relative;
		display: block;
		width: 1.05em;
		height: 1.55em;
		overflow: hidden;
		flex-shrink: 0;
	}
	.symbol img {
		position: absolute;
		width: 3.5em;
		max-width: none;
		height: 3.5em;
		left: -1.25em;
		top: -0.92em;
		filter: invert(1);
		mix-blend-mode: multiply;
	}
	:global(.dark) .symbol img,
	.mono .symbol img {
		filter: none;
		mix-blend-mode: screen;
	}
	.mono {
		color: hsl(var(--poster-paper));
	}
</style>
