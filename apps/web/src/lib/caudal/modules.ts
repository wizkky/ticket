import { env } from '$env/dynamic/public';

// Presentation only: historical records, APIs and their permission checks remain available.
export const showOptionalModules = env.PUBLIC_CAUDAL_SHOW_OPTIONAL_MODULES === 'true';

export function showModuleLink(href: string): boolean {
	return (
		showOptionalModules ||
		!/(?:\/account\/(?:memberships|referral)|\/admin\/members|\/org\/[^/]+\/membership|\/referral\/apply)(?:\/|$)/.test(
			href
		)
	);
}
