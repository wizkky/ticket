<script lang="ts">
	import * as m from '$lib/paraglide/messages.js';
	import { Button } from '$lib/components/ui/button';
	import QrCameraScanner from './QrCameraScanner.svelte';
	import * as Dialog from '$lib/components/ui/dialog';

	/**
	 * Dialog wrapper around `QrCameraScanner`. Everything camera-shaped — the
	 * getUserMedia lifecycle, the front-camera fallback, the per-error copy and
	 * the manual-entry fallback — lives in that component, which the org door page
	 * embeds without a dialog around it.
	 *
	 * Single-shot by design: the parent closes this modal in response to a scan,
	 * so the camera stays stopped rather than resuming (`continuous` is off).
	 */
	interface Props {
		isOpen: boolean;
		onClose: () => void;
		onScan: (ticketId: string) => Promise<void>;
	}

	const { isOpen, onClose, onScan }: Props = $props();
</script>

<Dialog.Root
	open={isOpen}
	onOpenChange={(open) => {
		if (!open) onClose();
	}}
>
	<Dialog.Content class="max-h-[90dvh] overflow-y-auto border shadow-none">
		<Dialog.Header>
			<Dialog.Title>{m['qrScannerModal.scanQr']()}</Dialog.Title>
			<Dialog.Description>{m['qrScannerModal.instructions']()}</Dialog.Description>
		</Dialog.Header>
		{#if isOpen}<QrCameraScanner active={isOpen} {onScan} />{/if}
		<Dialog.Footer
			><Button variant="outline" onclick={onClose}>{m['qrScannerModal.cancel']()}</Button
			></Dialog.Footer
		>
	</Dialog.Content>
</Dialog.Root>
