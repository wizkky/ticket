import type { PageServerLoad } from './$types';
import { eventpublicdiscoveryListEvents } from '$lib/api';
import { log } from '$lib/server/logger';
import type { EventOffer } from '$lib/caudal/offers';
import { loadOffers } from '$lib/server/caudal/offers';

export const load: PageServerLoad = async ({ fetch }) => {
	try {
		const response = await eventpublicdiscoveryListEvents({
			fetch,
			query: { region: 'los-rios', page_size: 3, order_by: 'start', include_past: false },
			signal: AbortSignal.timeout(5000)
		});
		if (response.error || !response.data) throw new Error('Public discovery unavailable');
		return {
			events: response.data.results,
			offers: await loadOffers(response.data.results, fetch),
			eventsUnavailable: false
		};
	} catch {
		log.warning('caudal_home_events_unavailable');
		return { events: [], offers: {} as Record<string, EventOffer>, eventsUnavailable: true };
	}
};
