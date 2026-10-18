import type { TicketTierSchema } from '$lib/api';
export interface EventOffer {
	amount: number | null;
	currency: string | null;
	free: boolean;
	door: boolean;
	soldOut: boolean;
}

/** Compute only from public tiers returned by the API. Do not infer eligibility from login. */
export function summarizeOffer(
	tiersIn: TicketTierSchema[],
	full = false,
	now = Date.now()
): EventOffer {
	const tiers = tiersIn.filter(
		(tier) =>
			!tier.sales_paused &&
			(!tier.sales_start_at || Date.parse(tier.sales_start_at) <= now) &&
			(!tier.sales_end_at || Date.parse(tier.sales_end_at) > now) &&
			tier.total_available !== 0
	);
	const prices = tiers
		.filter((tier) => !tier.seat_pricing)
		.map((tier) => ({
			amount: Number(tier.price_type === 'pwyc' ? tier.pwyc_min : tier.price),
			currency: tier.currency
		}))
		.filter((price) => Number.isFinite(price.amount));
	const currencies = new Set(prices.map((price) => price.currency));
	const cheapest = currencies.size === 1 ? prices.sort((a, b) => a.amount - b.amount)[0] : null;
	return {
		amount: cheapest?.amount ?? null,
		currency: cheapest?.currency ?? null,
		free: tiers.some((tier) => tier.payment_method === 'free'),
		door: tiers.some((tier) => tier.payment_method === 'at_the_door'),
		soldOut: full || (tiersIn.length > 0 && tiersIn.every((tier) => tier.total_available === 0))
	};
}
