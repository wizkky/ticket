import { buildSeo } from '$lib/seo';
import { resolveLang } from '$lib/seo/server';
import type { PageServerLoad } from './$types';
import { eventpublicdiscoveryListEvents } from '$lib/api';
import { loadCommunity } from '$lib/server/caudal/community';
import { log } from '$lib/server/logger';
import type { EventOffer } from '$lib/caudal/offers';
import { loadOffers } from '$lib/server/caudal/offers';

async function loadActivities(fetch: typeof globalThis.fetch) {
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
}

export const load: PageServerLoad = async ({ fetch, url, request }) => {
	const [activities, community] = await Promise.all([loadActivities(fetch), loadCommunity(fetch)]);
	return {
		...activities,
		...community,
		seo: buildSeo({ kind: 'home', url, lang: resolveLang(request) })
	};
};
