import { describe, expect, it } from 'vitest';
import type { CitySchema, TicketTierSchema } from '$lib/api';
import { summarizeOffer } from './offers';
import { countActiveFilters, hasActiveFilters, filtersToApiParams } from '$lib/utils/filters';
import { isLosRios } from './territory';
const tier = (overrides: Partial<TicketTierSchema> = {}): TicketTierSchema => ({
	id: 'tier',
	event_id: 'event',
	name: 'General',
	price: '10.00',
	currency: 'EUR',
	total_available: 5,
	seat_assignment_mode: 'none',
	payment_method: 'at_the_door',
	...overrides
});
const city = (country: string, region: string) => ({ country, admin_name: region }) as CitySchema;
describe('Caudal event territory', () => {
	it('accepts the existing Chilean region with or without accents', () => {
		expect(isLosRios(city('Chile', 'Los Ríos'))).toBe(true);
		expect(isLosRios(city('Chile', 'Los Rios'))).toBe(true);
	});
	it('rejects other regions, countries and missing event location', () => {
		expect(isLosRios(city('Chile', 'Metropolitana'))).toBe(false);
		expect(isLosRios(city('Argentina', 'Los Ríos'))).toBe(false);
		expect(isLosRios(null)).toBe(false);
	});
});
describe('public ticket offers', () => {
	it('keeps real free and pay-at-door options visible for anonymous buyers', () => {
		expect(
			summarizeOffer([tier({ can_purchase: false }), tier({ price: '0', payment_method: 'free' })])
		).toEqual({ amount: 0, currency: 'EUR', free: true, door: true, soldOut: false });
	});
	it('excludes paused, unavailable and future sales from the starting price', () => {
		const offer = summarizeOffer([
			tier(),
			tier({ price: '1', sales_paused: true }),
			tier({ price: '0', total_available: 0 }),
			tier({ price: '2', sales_start_at: '2099-01-01T00:00:00Z' })
		]);
		expect(offer.amount).toBe(10);
	});
	it('never combines different currencies into a misleading minimum', () => {
		expect(summarizeOffer([tier(), tier({ currency: 'USD', price: '3' })]).amount).toBeNull();
	});
	it('reports sold-out capacity and handles missing or complex prices without invented zeros', () => {
		expect(summarizeOffer([tier({ total_available: 0 })]).soldOut).toBe(true);
		expect(summarizeOffer([]).amount).toBeNull();
		expect(summarizeOffer([tier({ price: 'invalid' })]).amount).toBeNull();
	});
	it('uses the actual pay-what-you-can minimum', () => {
		expect(summarizeOffer([tier({ price_type: 'pwyc', pwyc_min: '4.50' })]).amount).toBe(4.5);
	});
});

describe('territorial discovery defaults', () => {
	it('uses the event date without showing a fictitious active filter', () => {
		expect(filtersToApiParams({}).order_by).toBe('start');
		expect(countActiveFilters({ orderBy: 'start' })).toBe(0);
		expect(hasActiveFilters({ orderBy: 'start' })).toBe(false);
		expect(countActiveFilters({ orderBy: 'start', cityId: 53 })).toBe(1);
	});
});
