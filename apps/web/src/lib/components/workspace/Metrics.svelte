<script lang="ts">
	import type { CaudalMetrics } from '$lib/api';
	import * as m from '$lib/paraglide/messages.js';
	const { metrics }: { metrics: CaudalMetrics } = $props();
	const items = $derived([
		{ label: m['workspace.issued'](), value: metrics.issued },
		{ label: m['workspace.reservations'](), value: metrics.door_reservations },
		{ label: m['workspace.admissions'](), value: metrics.admissions },
		{ label: m['workspace.payments'](), value: metrics.online_payments }
	]);
</script>

<div class="metrics">
	{#each items as item (item.label)}<div>
			<span class="metric-label">{item.label}</span><strong>{item.value}</strong>
		</div>{/each}
</div>
<p class="metric-note">{m['workspace.metricsHint']()}</p>

<style>
	.metrics {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		border-block: 1px solid hsl(var(--border));
		margin-top: 35px;
	}
	.metrics > div {
		padding: 25px 22px;
		border-right: 1px solid hsl(var(--border));
	}
	.metrics > div:first-child {
		padding-left: 0;
	}
	.metrics > div:last-child {
		border-right: 0;
	}
	.metric-label {
		display: block;
		font-size: 11px;
		color: hsl(var(--muted-foreground));
		line-height: 1.6;
		min-height: 36px;
	}
	strong {
		display: block;
		font-family: 'Manrope', sans-serif;
		font-size: 48px;
		font-weight: 400;
		letter-spacing: -0.06em;
		line-height: 1.3;
	}
	.metric-note {
		font-size: 11px;
		line-height: 1.8;
		color: hsl(var(--muted-foreground));
		max-width: 760px;
		margin-top: 16px;
	}
	@media (max-width: 640px) {
		.metrics {
			grid-template-columns: 1fr 1fr;
		}
		.metrics > div {
			padding: 20px 14px !important;
		}
		.metrics > div:nth-child(2) {
			border-right: 0;
		}
		.metrics > div:nth-child(-n + 2) {
			border-bottom: 1px solid hsl(var(--border));
		}
		strong {
			font-size: 40px;
		}
	}
</style>
