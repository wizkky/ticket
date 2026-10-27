import { describe, expect, it } from 'vitest';
import { moneyInputPattern, moneyInputValue, normalizeMoneyInput } from './money-input';

describe('CLP price inputs', () => {
	it.each(['5500', '5.500', '$5.500', '$ 5.500'])('accepts %s as whole pesos', (value) => {
		expect(normalizeMoneyInput(value, 'CLP')).toBe('5500');
	});
	it('keeps fractional input invalid instead of multiplying it', () => {
		const value = normalizeMoneyInput('5000.50', 'CLP');
		expect(value).toBe('5000.50');
		expect(new RegExp(`^(?:${moneyInputPattern('CLP')})$`).test(value)).toBe(false);
	});
	it('removes only zero fractional digits from stored CLP', () => {
		expect(moneyInputValue('5500.00', 'CLP')).toBe('5500');
		expect(moneyInputValue('12.50', 'EUR')).toBe('12.50');
	});
});
