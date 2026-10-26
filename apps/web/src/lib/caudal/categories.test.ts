import { describe, expect, it } from 'vitest';
import { CATEGORY_TAGS, activityCategories, categoryTags, parseCategory } from './categories';
import {
	parseFilters,
	filtersToParams,
	filtersToApiParams,
	clearFilters,
	countActiveFilters
} from '$lib/utils/filters';
import { formatMoney } from '$lib/utils/format';
import { moneyInputValue, normalizeMoneyInput } from '$lib/utils/money-input';

describe('creative discovery categories', () => {
	it('defines eight distinct interests backed by real API tag filters', () => {
		const categories = activityCategories();
		expect(categories).toHaveLength(8);
		expect(new Set(categories.map((category) => category.id)).size).toBe(8);
		for (const category of categories) {
			expect(category.label.length).toBeGreaterThan(0);
			expect(categoryTags(category.id)).toEqual([...CATEGORY_TAGS[category.id]]);
		}
	});
	it.each(['unknown', '__proto__', 'constructor', 'toString', 'MUSICA', null, undefined])(
		'ignores an unsupported category: %s',
		(value) => {
			expect(parseCategory(value)).toBeUndefined();
		}
	);
	it('preserves a category through other filters and pagination', () => {
		const filters = parseFilters(
			new URLSearchParams('category=escena&city_id=53&search=cine&page=2')
		);
		expect(filters.category).toBe('escena');
		const url = filtersToParams({ ...filters, page: 3 });
		expect(url.get('category')).toBe('escena');
		expect(url.get('city_id')).toBe('53');
		expect(url.get('search')).toBe('cine');
		expect(url.get('page')).toBe('3');
		expect(filtersToApiParams(filters).tags).toEqual([...CATEGORY_TAGS.escena]);
	});
	it('counts a category once and clears it without changing the chronological default', () => {
		expect(countActiveFilters({ category: 'musica', orderBy: 'start' })).toBe(1);
		expect(filtersToParams(clearFilters()).get('category')).toBeNull();
		expect(filtersToApiParams(clearFilters()).order_by).toBe('start');
	});
	it('keeps custom API tags when no editorial category is selected', () => {
		expect(categoryTags(undefined, ['demo'])).toEqual(['demo']);
		expect(categoryTags(undefined)).toBeUndefined();
	});
});

describe('CLP continuity during the creative redesign', () => {
	it('renders whole Chilean pesos with a period for thousands', () => {
		expect(formatMoney('5000.00', 'CLP')).toBe('$5.000');
		expect(formatMoney('5500', 'CLP')).toBe('$5.500');
	});
	it('accepts pasted Chilean prices without silently converting fractional pesos', () => {
		expect(normalizeMoneyInput('$5.500', 'CLP')).toBe('5500');
		expect(normalizeMoneyInput('5000.50', 'CLP')).toBe('5000.50');
		expect(moneyInputValue('5000.00', 'CLP')).toBe('5000');
	});
});
