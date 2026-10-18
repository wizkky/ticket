import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { caudalDoor } from '$lib/api';
import * as m from '$lib/paraglide/messages.js';
export const load: PageServerLoad = async ({ params, fetch, locals, parent }) => {
	await parent();
	const result = await caudalDoor({
		fetch,
		path: { event_id: params.event_id },
		headers: { Authorization: `Bearer ${locals.user?.accessToken}` }
	});
	if (!result.data) error(result.response?.status === 403 ? 403 : 404, m['workspace.protected']());
	if (result.data.organization_slug !== params.slug) error(404, m['workspace.protected']());
	return { event: result.data };
};
