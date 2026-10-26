import { organizationListOrganizations } from '$lib/api';
import type { OrganizationRetrieveSchema } from '$lib/api';
import { isLosRios } from '$lib/caudal/territory';

/** Public regional preview, not a complete directory or a list of partner organizations. */
export async function loadCommunity(fetchFn: typeof fetch) {
	try {
		const response = await organizationListOrganizations({
			fetch: fetchFn,
			query: { page_size: 20, order_by: 'name' },
			signal: AbortSignal.timeout(5000)
		});
		if (!response.data || response.error) throw new Error('Community unavailable');
		return {
			organizations: response.data.results.filter((org) => isLosRios(org.city)).slice(0, 3),
			communityUnavailable: false
		};
	} catch {
		return { organizations: [] as OrganizationRetrieveSchema[], communityUnavailable: true };
	}
}
