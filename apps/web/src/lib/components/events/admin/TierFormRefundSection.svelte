<script lang="ts">
	import * as m from '$lib/paraglide/messages.js';
	import type { RefundPolicy } from '$lib/api/generated/types.gen';
	import { DurationInput } from '$lib/components/forms';
	import RefundPolicyEditor from './RefundPolicyEditor.svelte';
	import { Undo2 } from '@lucide/svelte';
	interface Props {
		allowUserCancellation: boolean;
		cancellationDeadlineHours: number | null;
		refundPolicy: RefundPolicy | null;
		onValidityChange: (valid: boolean) => void;
		currency: string;
		currencySymbol: string;
		isPending: boolean;
	}
	let {
		allowUserCancellation = $bindable(),
		cancellationDeadlineHours = $bindable(),
		refundPolicy = $bindable(),
		onValidityChange,
		currency,
		currencySymbol,
		isPending
	}: Props = $props();
</script>

<div class="space-y-4 rounded-lg border border-border bg-muted/30 p-4">
	<div class="flex items-center gap-2 text-sm font-medium">
		<Undo2 class="h-4 w-4 text-primary" aria-hidden="true" />
		{m['refundPolicy.sectionTitle']()}
	</div>

	<label class="flex cursor-pointer items-start gap-2">
		<input
			type="checkbox"
			bind:checked={allowUserCancellation}
			disabled={isPending}
			class="mt-0.5 h-4 w-4 rounded border-input text-primary focus:ring-2 focus:ring-primary"
		/>
		<div>
			<span class="text-sm font-medium">
				{m['refundPolicy.allowCancellationLabel']()}
			</span>
			<p class="text-xs text-muted-foreground">
				{m['refundPolicy.allowCancellationHelp']()}
			</p>
		</div>
	</label>

	{#if allowUserCancellation}
		<DurationInput
			id="cancellation-deadline-hours"
			label={m['refundPolicy.deadlineLabel']()}
			helpText={m['refundPolicy.deadlineHelp']()}
			bind:value={cancellationDeadlineHours}
			storageUnit="hours"
			defaultUnit="days"
			emptyValue={null}
			emptyLabel={m['refundPolicy.deadlineNoLimit']()}
			disabled={isPending}
		/>

		<RefundPolicyEditor
			{currency}
			value={refundPolicy}
			disabled={isPending}
			{currencySymbol}
			onChange={(next) => (refundPolicy = next)}
			{onValidityChange}
		/>
	{/if}
</div>
