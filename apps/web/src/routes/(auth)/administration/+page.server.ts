import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { caudalAdministration } from '$lib/api';
import { getBackendUrl } from '$lib/config/api';
import * as m from '$lib/paraglide/messages.js';
export const load: PageServerLoad = async ({ locals, fetch }) => {
	if (!locals.user?.accessToken) redirect(303, '/login?returnUrl=%2Fadministration');
	const response = await caudalAdministration({
		fetch,
		headers: { Authorization: `Bearer ${locals.user.accessToken}` },
		signal: AbortSignal.timeout(8000)
	}).catch(() => null);
	if (!response) error(503, m['workspace.dataUnavailable']());
	if (response.response?.status === 403) error(403, m['workspace.forbidden']());
	if (!response.data) error(503, m['workspace.dataUnavailable']());
	return {
		overview: response.data,
		tools: response.data.sections.map((section) => ({
			...section,
			href: getBackendUrl(section.path)
		}))
	};
};
