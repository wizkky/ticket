import { describe, expect, it } from 'vitest';
import { showModuleLink } from './modules';

describe('optional modules hidden in this trial', () => {
	it.each([
		'/account/memberships',
		'/account/referral/payouts',
		'/org/caudal-demo-a/admin/members',
		'/org/caudal-demo-a/membership',
		'/referral/apply'
	])('hides %s', (href) => expect(showModuleLink(href)).toBe(false));

	it.each(['/account/profile', '/org/caudal-demo-a/admin/tickets', '/dashboard/tickets'])(
		'keeps %s',
		(href) => expect(showModuleLink(href)).toBe(true)
	);
});
