<script lang="ts">
	// Shared interface retained for upstream consumers; artwork is the supplied, unmodified logo.
	import { asset } from '$app/paths';
	import { cn } from '$lib/utils';
	interface Props {
		class?: string;
		mono?: boolean;
		mark?: boolean;
	}
	const { class: className = '', mono = false }: Props = $props();
</script>

<span class={cn('caudal-wordmark', mono && 'mono', className)}>
	<!-- i18n-ignore: supplied brand name -->
	<img src={asset('/brand/caudal/creative.png')} alt="Caudal Creativo" width="2048" height="682" />
</span>

<style>
	.caudal-wordmark {
		display: inline-flex;
		align-items: center;
		width: 8em;
		max-width: 100%;
		vertical-align: middle;
	}
	img {
		width: 100%;
		height: auto;
		filter: invert(1);
		mix-blend-mode: multiply;
	}
	:global(.dark) img,
	.mono img {
		filter: none;
		mix-blend-mode: screen;
	}
</style>
