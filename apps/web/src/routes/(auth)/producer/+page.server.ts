import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { resolve } from '$app/paths';
export const load: PageServerLoad = async ({ locals, parent }) => {
	if (!locals.user) redirect(303, resolve('/(public)/login', {}) + '?returnUrl=%2Fproducer');
	const data = await parent();
	return { workspace: data.workspace, canCreateOrganization: data.features.organization_creation };
};
