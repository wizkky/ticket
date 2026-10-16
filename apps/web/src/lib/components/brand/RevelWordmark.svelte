<script lang="ts">
	// Keep the upstream component interface so every shared navigation surface
	// uses the CaudalTickets prototype wordmark without changing its callers.
	import { cn } from '$lib/utils';

	interface Props {
		class?: string;
		mono?: boolean;
		/** Retained for compatibility; this prototype uses a text-only identity. */
		mark?: boolean;
	}
	const { class: className = '', mono = false }: Props = $props();
</script>

<span class={cn('inline-flex items-center whitespace-nowrap text-2xl leading-none', className)}>
	<!-- i18n-ignore: product name -->
	<span class="font-extrabold">Caudal</span>
	<!-- i18n-ignore: product name -->
	<span class={mono ? 'font-semibold' : 'font-semibold text-primary'}>Tickets</span>
</span>
