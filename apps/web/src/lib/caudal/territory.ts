import type { CitySchema } from '$lib/api';
/** Event territory is independent of account/profile location. */
export function isLosRios(city: CitySchema | null | undefined): boolean {
	const normalized = (value: string) =>
		value
			.normalize('NFD')
			.replace(/\p{Diacritic}/gu, '')
			.toLowerCase();
	return (
		!!city &&
		['chile', 'cl'].includes(normalized(city.country)) &&
		/los\s+rios/.test(normalized(city.admin_name ?? ''))
	);
}
