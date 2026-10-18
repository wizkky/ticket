import { eventpublicticketsListTiers, type EventInListSchema } from '$lib/api';
import { summarizeOffer, type EventOffer } from '$lib/caudal/offers';
/** Public-tier endpoint preserves visibility and capacity disclosure rules. */
export async function loadOffers(
	events: EventInListSchema[],
	fetcher: typeof fetch,
	token?: string
): Promise<Record<string, EventOffer>> {
	const entries = await Promise.all(
		events.slice(0, 20).map(async (event) => {
			try {
				const result = await eventpublicticketsListTiers({
					fetch: fetcher,
					path: { event_id: event.id },
					headers: token ? { Authorization: `Bearer ${token}` } : {},
					signal: AbortSignal.timeout(5000)
				});
				if (!result.data) return null;
				const offer = summarizeOffer(result.data, !!event.is_full);
				return [event.id, offer] as const;
			} catch {
				return null;
			}
		})
	);
	return Object.fromEntries(
		entries.filter((entry): entry is readonly [string, EventOffer] => entry !== null)
	);
}
