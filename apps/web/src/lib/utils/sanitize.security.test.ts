import { describe, expect, it } from 'vitest';
import { sanitizeHtml } from './sanitize';

describe('HTML sanitization at the event-description boundary', () => {
	it('removes executable tags and handlers while preserving readable content', () => {
		const output = sanitizeHtml(
			'<p>Event details</p><script>alert(1)</script>' +
				'<img src="x" onerror="alert(1)"><a href="javascript:alert(1)" onclick="alert(1)">Tickets</a>'
		);

		expect(output).toContain('<p>Event details</p>');
		expect(output).toContain('Tickets');
		expect(output).not.toMatch(/<script|<img|onerror|onclick|javascript:/i);
	});

	it('removes encoded executable URLs and embedded documents', () => {
		const output = sanitizeHtml(
			'<a href="java&#x73;cript:alert(1)">Entry</a>' +
				'<iframe srcdoc="<script>alert(1)</script>"></iframe><svg onload="alert(1)"></svg>'
		);

		expect(output).toContain('Entry');
		expect(output).not.toMatch(/href=|<iframe|<svg|srcdoc|onload/i);
	});

	it('preserves safe event formatting and ordinary HTTPS links', () => {
		const output = sanitizeHtml(
			'<h2>Live music</h2><p><strong>Doors open</strong></p>' +
				'<a href="https://example.com/tickets" data-internal="private">Book</a>'
		);

		expect(output).toContain('<h2>Live music</h2>');
		expect(output).toContain('<strong>Doors open</strong>');
		expect(output).toContain('href="https://example.com/tickets"');
		expect(output).not.toContain('data-internal');
	});
});
