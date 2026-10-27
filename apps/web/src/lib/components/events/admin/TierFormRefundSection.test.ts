import { render, screen } from '@testing-library/svelte';
import userEvent from '@testing-library/user-event';
import { expect, it, vi } from 'vitest';
import TierFormRefundSection from './TierFormRefundSection.svelte';

const props = {
	allowUserCancellation: false,
	cancellationDeadlineHours: null,
	refundPolicy: null,
	onValidityChange: vi.fn(),
	currency: 'CLP',
	currencySymbol: '$',
	isPending: false
};

it('shows and hides refund settings when cancellation is toggled', async () => {
	render(TierFormRefundSection, { props });
	const toggle = screen.getByRole('checkbox');
	expect(screen.queryByLabelText('Cancellation deadline before event')).not.toBeInTheDocument();
	await userEvent.click(toggle);
	expect(toggle).toBeChecked();
	expect(screen.getByText('Cancellation deadline before event')).toBeInTheDocument();
	await userEvent.click(toggle);
	expect(toggle).not.toBeChecked();
	expect(screen.queryByText('Cancellation deadline before event')).not.toBeInTheDocument();
});

it('blocks edits while saving', () => {
	render(TierFormRefundSection, { props: { ...props, isPending: true } });
	expect(screen.getByRole('checkbox')).toBeDisabled();
});
