import type { PageServerLoad } from './$types';
import { caudalProducerOverview } from '$lib/api';
export const load: PageServerLoad = async ({ locals, fetch, params, parent }) => {
	await parent();
	const response = await caudalProducerOverview({
		fetch,
		path: { slug: params.slug },
		headers: { Authorization: `Bearer ${locals.user?.accessToken}` },
		signal: AbortSignal.timeout(8000)
	}).catch(() => null);
	return { overview: response?.data ?? null };
};
