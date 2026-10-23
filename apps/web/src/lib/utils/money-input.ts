/** CLP accepts whole pesos and pasted Chilean thousands separators. */
export function normalizeMoneyInput(value: string, currency: string): string {
	if (currency.toUpperCase() === 'CLP') {
		const raw = value.replace(/\s/g, '').replace(/^\$/, '');
		// Do not turn a fractional amount such as 5000.50 into 500050 pesos.
		return /^\d{1,3}(\.\d{3})+$/.test(raw) ? raw.replace(/\./g, '') : raw;
	}
	let normalized = value.replace(/,/g, '.').replace(/[^\d.]/g, '');
	const dot = normalized.indexOf('.');
	if (dot !== -1)
		normalized = normalized.slice(0, dot + 1) + normalized.slice(dot + 1).replace(/\./g, '');
	return normalized;
}

export function moneyInputPattern(currency: string): string | undefined {
	return currency.toUpperCase() === 'CLP' ? '[0-9]+' : undefined;
}

/** Strip the API DecimalField's zero fractional digits when opening an editor. */
export function moneyInputValue(value: string, currency: string): string {
	return currency.toUpperCase() === 'CLP' ? value.replace(/\.0+$/, '') : value;
}
