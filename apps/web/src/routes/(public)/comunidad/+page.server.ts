import { eventpublicdiscoveryListEvents } from '$lib/api';
import type { EventInListSchema } from '$lib/api';
import { loadCommunity } from '$lib/server/caudal/community';
import type { PageServerLoad } from './$types';

async function loadSpaces(fetchFn: typeof fetch) {
	try {
		const response = await eventpublicdiscoveryListEvents({
			fetch: fetchFn,
			query: { region: 'los-rios', page_size: 20, include_past: false, order_by: 'start' },
			signal: AbortSignal.timeout(5000)
		});
		if (!response.data || response.error) throw new Error('Published activities unavailable');
		const venues = new Map<string, EventInListSchema>();
		for (const event of response.data.results) {
			if (event.venue?.id && !venues.has(event.venue.id)) venues.set(event.venue.id, event);
		}
		return { venueEvents: [...venues.values()].slice(0, 3), spacesUnavailable: false };
	} catch {
		return { venueEvents: [] as EventInListSchema[], spacesUnavailable: true };
	}
}

export const load: PageServerLoad = async ({ fetch }) => {
	const [community, spaces] = await Promise.all([loadCommunity(fetch), loadSpaces(fetch)]);
	return { ...community, ...spaces };
};
