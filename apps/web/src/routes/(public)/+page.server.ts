import type { PageServerLoad } from './$types';
import { eventpublicdiscoveryListEvents } from '$lib/api';
import { log } from '$lib/server/logger';

export const load: PageServerLoad = async ({ fetch }) => {
	try {
		const response = await eventpublicdiscoveryListEvents({
			fetch,
			query: { page_size: 3, order_by: 'start', include_past: false },
			signal: AbortSignal.timeout(5000)
		});
		if (response.error || !response.data) throw new Error('Public discovery unavailable');
		return { events: response.data.results, eventsUnavailable: false };
	} catch {
		log.warning('caudal_home_events_unavailable');
		return { events: [], eventsUnavailable: true };
	}
};
