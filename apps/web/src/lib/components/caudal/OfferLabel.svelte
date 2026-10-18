<script lang="ts">
	import type { EventOffer } from '$lib/caudal/offers';
	import { formatPrice } from '$lib/utils/format';
	import * as m from '$lib/paraglide/messages.js';
	const { offer }: { offer?: EventOffer } = $props();
</script>

<div class="offer-label">
	{#if offer?.soldOut}<span>{m['eventStatus.full']()}</span>
	{:else if offer?.amount !== null && offer?.amount !== undefined && offer.currency}
		<strong
			>{offer.free && offer.amount === 0
				? m['workspace.freeTicket']()
				: m['workspace.fromPrice']({ price: formatPrice(offer.amount, offer.currency) })}</strong
		>{#if offer.door}<span>{m['workspace.payDoor']()}</span>{/if}
	{:else}<span>{m['workspace.checkAvailability']()}</span>{/if}
</div>

<style>
	.offer-label {
		display: flex;
		align-items: center;
		flex-wrap: wrap;
		gap: 8px 14px;
		font-size: 11px;
		line-height: 1.5;
		margin-top: 16px;
	}
	strong {
		font-weight: 500;
	}
	.offer-label > span {
		color: hsl(var(--muted-foreground));
	}
</style>
